# Task Management API — Phase 1 to Phase 2 Evolution

A lightweight FastAPI and SQLite task management backend that evolved from a basic CRUD service into a production-grade, schema-validated LLM enrichment pipeline powered by **Groq** (`llama-3.3-70b-versatile`).

---

##  Assignment 1 vs Assignment 2 (What Changed?)

###  Assignment 1 (Phase 1: Basic CRUD API)
* What Was Built: A standard Task Management Backend API using FastAPI and SQLite.
* Endpoints:
  * `GET /tasks` - Retrieve all tasks
  * `GET /tasks/{id}` - Fetch a single task by ID
  * `POST /tasks` - Create a new task
  * `PUT /tasks/{id}` - Update an existing task
  * `DELETE /tasks/{id}` - Delete a task
* Limitations: Contains no AI features. Whatever task title the user submits is stored directly into the database as-is.

---

###  Assignment 2 (Phase 2: Resilient Groq LLM Pipeline)
* What Was Added: Integrated a new **`POST /tasks/{task_id}/enrich`** AI endpoint directly into the existing CRUD application.
* What It Does: Fetches a task title from SQLite and asks Groq LLM to automatically categorize and enrich it into structured JSON:
* Category: (`work`, `learning`, `personal`, `admin`, `other`)
* Priority: (`low`, `medium`, `high`)
* Estimated Minutes:** Estimated completion time (integer: 1–480)
* Confidence Score:** Model certainty score (float: 0.0–1.0)
* Reasoning: Concise explanation string
* Reliability & Resilience Guardrails:**
* Schema Safety: Response shapes are strictly validated using Pydantic models.
  * 1 Repair Retry: If the LLM generates invalid JSON, the code sends the validation error back to the model once for self-repair.
  * Timeout & Backoff: Configured with a strict 10s timeout and exponential backoff retries for rate-limit errors (429/5xx).
  * Quarantine Logging: Unrepairable failures write raw outputs to `logs/quarantine.jsonl` and return a clean `422 Unprocessable Entity`.
  * Kill Switch & Stub: Supports instant model disablement via `LLM_ENABLED=false` and offline testing via `LLM_STUB=1`.

---

## Runnable Examples

### 1. Fetch Basic Tasks (Assignment 1)
```bash
curl [http://127.0.0.1:8000/tasks](http://127.0.0.1:8000/tasks)

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install fastapi uvicorn pydantic requests groq python-dotenv
uvicorn main:app --reload

curl [http://127.0.0.1:8000/tasks](http://127.0.0.1:8000/tasks)

curl -X POST [http://127.0.0.1:8000/tasks/1/enrich](http://127.0.0.1:8000/tasks/1/enrich)

python evals/run_eval.py