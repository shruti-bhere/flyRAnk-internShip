import sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()
DB_FILE = "tasks.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def startup():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER DEFAULT 0
            )
        """)
        cursor.execute("SELECT COUNT(*) AS count FROM tasks")
        if cursor.fetchone()["count"] == 0:
            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                [
                    ("Buy groceries", 0),
                    ("Walk the dog", 1),
                    ("Complete Week 2 assignment", 0)
                ]
            )
        conn.commit()

class TaskCreate(BaseModel):
    title: str
    done: Optional[bool] = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

def format_task(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

@app.get("/tasks")
def get_tasks(search: Optional[str] = None, done: Optional[bool] = None):
    query = "SELECT * FROM tasks"
    params = []
    conditions = []

    if search:
        conditions.append("title LIKE ?")
        params.append(f"%{search}%")
    if done is not None:
        conditions.append("done = ?")
        params.append(1 if done else 0)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [format_task(row) for row in rows]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        return format_task(row)

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    if not task.title or task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (task.title.strip(), 1 if task.done else 0)
        )
        conn.commit()
        task_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return format_task(cursor.fetchone())

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Task not found")

        updated_title = task.title.strip() if task.title is not None else existing["title"]
        if task.title is not None and updated_title == "":
            raise HTTPException(status_code=400, detail="Title cannot be empty")

        updated_done = (1 if task.done else 0) if task.done is not None else existing["done"]

        cursor.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (updated_title, updated_done, task_id)
        )
        conn.commit()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return format_task(cursor.fetchone())

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/stats")
def get_stats():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS count FROM tasks")
        total = cursor.fetchone()["count"]
        cursor.execute("SELECT COUNT(*) AS count FROM tasks WHERE done = 1")
        completed = cursor.fetchone()["count"]
        return {"total": total, "completed": completed, "pending": total - completed}