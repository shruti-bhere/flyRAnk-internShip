import os
import json
import time
import re
import sqlite3
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
DB_NAME = "tasks.db"

# --- Database Helper Functions ---

def get_db():
    """Returns a SQLite connection with dict-like row access."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the tasks table and seeds initial tasks if empty."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        
        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]
        
        if count == 0:
            seed_tasks = [
                ("Learn SQLite parameterized queries", 0),
                ("Build FastAPI CRUD endpoints", 1),
                ("Inspect database in DB Browser", 0)
            ]
            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)", 
                seed_tasks
            )
            conn.commit()

# --- Application Lifespan ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure logs directory exists for quarantine logs
    os.makedirs("logs", exist_ok=True)
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# --- Groq SDK Client Setup ---

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("LLM_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GROQ_API_KEY environment variable is not set."
        )
    return Groq(api_key=api_key)

# --- Request / Response Models ---

class TaskCreate(BaseModel):
    title: str
    done: Optional[bool] = False

class TaskUpdate(BaseModel):
    title: str
    done: bool

class TaskEnrichmentOutput(BaseModel):
    category: str = Field(description="Must be one of: work, learning, personal, admin, other")
    priority: str = Field(description="Must be one of: low, medium, high")
    estimated_minutes: int = Field(description="Estimated time in minutes (1 to 480)")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    reasoning: str = Field(description="One short sentence explaining the choice")

# --- Resilient Groq LLM Helper Function ---

def call_llm_with_resilience(task_title: str) -> dict:
    # 1. Kill switch check
    if os.getenv("LLM_ENABLED", "true").lower() == "false":
        return {
            "category": "other",
            "priority": "low",
            "estimated_minutes": 15,
            "confidence": 0.0,
            "reasoning": "LLM feature disabled via kill switch."
        }

    # 2. Stub mode check
    if os.getenv("LLM_STUB", "0") == "1":
        return {
            "category": "learning",
            "priority": "medium",
            "estimated_minutes": 30,
            "confidence": 0.95,
            "reasoning": "Stub response generated without API call."
        }

    # Load versioned prompt from file
    prompt_file = os.path.join("prompts", "job-v1.md")
    if os.path.exists(prompt_file):
        with open(prompt_file, "r") as f:
            system_prompt = f.read()
    else:
        system_prompt = (
            "You are a backend task classification pipeline. "
            "Output ONLY a JSON object matching this schema:\n"
            "{\n"
            '  "category": "work|learning|personal|admin|other",\n'
            '  "priority": "low|medium|high",\n'
            '  "estimated_minutes": integer (1-480),\n'
            '  "confidence": float (0.0-1.0),\n'
            '  "reasoning": "one short sentence"\n'
            "}\n"
            "Rules: Output ONLY valid JSON. If unsure, set category to 'other', priority to 'low', and confidence < 0.5."
        )

    # Prevent prompt injection by placing untrusted content into user role JSON payload
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps({"task_title": task_title})}
    ]

    raw_output = _execute_groq_call(messages)
    
    # Parse & validate response
    try:
        cleaned = re.sub(r"```json|```", "", raw_output).strip()
        validated = TaskEnrichmentOutput.model_validate_json(cleaned)
        return validated.model_dump()
    except Exception as validation_err:
        # Single Repair Retry: Hand model its broken answer + error
        repair_messages = [
            *messages,
            {"role": "assistant", "content": raw_output},
            {
                "role": "user", 
                "content": f"Your output failed JSON validation: {str(validation_err)}. Please return ONLY corrected valid JSON."
            }
        ]
        
        try:
            repaired_output = _execute_groq_call(repair_messages)
            cleaned_repair = re.sub(r"```json|```", "", repaired_output).strip()
            validated = TaskEnrichmentOutput.model_validate_json(cleaned_repair)
            return validated.model_dump()
        except Exception as final_err:
            # Quarantine on failure
            quarantine_path = os.path.join("logs", "quarantine.jsonl")
            with open(quarantine_path, "a") as qf:
                qf.write(json.dumps({
                    "input": task_title,
                    "raw_output": raw_output,
                    "error": str(final_err)
                }) + "\n")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Model response failed schema validation after repair attempt."
            )

def _execute_groq_call(messages: list, max_retries: int = 3) -> str:
    """Executes Groq API call with strict 10s timeout, response_format, and exponential backoff."""
    client = get_groq_client()
    model_name = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.2,
                response_format={"type": "json_object"},  # Native Groq JSON enforcement
                timeout=10.0                              # Strict 10s timeout
            )
            return response.choices[0].message.content
        except Exception as err:
            status_code = getattr(err, "status_code", None)
            
            # Fail fast on client authentication / bad parameter errors (400, 401, 403)
            if status_code and 400 <= status_code < 500 and status_code != 429:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Groq Client Error: {str(err)}"
                )
            
            if attempt == max_retries - 1:
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail="Groq service failed or timed out after max retries."
                )
            
            time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s

# --- API Endpoints ---

@app.get("/tasks")
def get_tasks():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, done FROM tasks")
        rows = cursor.fetchall()
        return [
            {"id": row["id"], "title": row["title"], "done": bool(row["done"])}
            for row in rows
        ]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task not found"
            )
            
        return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    clean_title = task.title.strip()
    if not clean_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Title cannot be empty"
        )
        
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (clean_title, int(task.done))
        )
        conn.commit()
        new_id = cursor.lastrowid
        
    return {"id": new_id, "title": clean_title, "done": task.done}

# --- GROQ ENRICHMENT ENDPOINT ---

@app.post("/tasks/{task_id}/enrich", response_model=TaskEnrichmentOutput)
def enrich_task(task_id: int):
    """Fetches task title from SQLite and asks Groq to classify and enrich it."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        task_title = row["title"]

    if not task_title or len(task_title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title is invalid or empty"
        )

    return call_llm_with_resilience(task_title)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    clean_title = task.title.strip()
    if not clean_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Title cannot be empty"
        )
        
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (clean_title, int(task.done), task_id)
        )
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task not found"
            )
            
    return {"id": task_id, "title": clean_title, "done": task.done}

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task not found"
            )
            
    return Response(status_code=status.HTTP_204_NO_CONTENT)