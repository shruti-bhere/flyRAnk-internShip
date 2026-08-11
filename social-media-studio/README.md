#  Social Media Studio - Multi-Agent Engine & Background Worker Architecture

This repository documents the evolution of **Social Media Studio**, starting from a synchronous multi-agent content engine to an asynchronous **HTTP 202 Background Job Worker Architecture**.

---

##  Project Evolution & Architecture Journey

### Phase 1: Initial Core Engine (Assignment 1 - Synchronous Pipeline)
* What was built: A multi-agent AI pipeline built using LangGraph, LangChain, and local Ollama models (`llama3`).
* The Workflow: 
  `User Request` ──► `Researcher Agent` ──► `Writer Agent` ──► `Reviewer Agent` ──► `Final Post`
* The Limitation: The API was Synchronous (`POST /generate`)**. The client had to wait 10-15 seconds with an open HTTP connection while the AI agents finished researching, drafting, and reviewing. This caused slow user experience and potential request timeouts.

---

### Phase 2: Architectural Upgrade (Assignment 2 / BE-06 - Async Background Jobs)
* Why it was upgraded: Real-world AI applications must never block the API thread during slow operations. We decoupled the API request from the AI processing using an asynchronous worker queue.
* What was added/updated:
  1. HTTP 202 Accepted Endpoint (`POST /jobs/generate`): Accepts requests instantly (<1 second) and returns a unique `job_id` and tracking status URL.
  2. Background Worker Execution (`app/worker.py`): Offloads the heavy multi-agent LangGraph workflow to a background thread via FastAPI `BackgroundTasks`.
  3. State Engine & In-Memory Queue (`app/queue.py`): Tracks job status through stages (`pending` ──► `processing` ──► `completed` / `failed`).
  4. Status Polling Endpoint (`GET /jobs/{job_id}`): Allows clients to poll job progress and fetch final generated content when ready.
  5. Resiliency & Retries: Added exponential backoff retries (up to 3 attempts) and idempotency checks to prevent duplicate executions.

---

## 🏗️ System Architecture Flow

```text
1. Client POST /jobs/generate ──► Return HTTP 202 Accepted { job_id, status: "pending" }
                                           │
                                           ▼
                                 [ Background Worker ]
                                           │
                                (Executes Agent Workflow)
                                           │
                                           ▼
2. Client GET /jobs/{job_id} ──► Status: "processing" ──► "completed" { result }

MAC
python3 -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

ollama pull llama3
ollama pull nomic-embed-text

uvicorn app.main:app --reload --port 8000
http://localhost:8000/docs


Testing the Upgraded Async API

curl -X POST "http://localhost:8000/jobs/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "topic": "Agentic AI Workflows in LangGraph",
       "target_platform": "LinkedIn"
     }'

Response

{
  "job_id": "c0fee277-dcd8-44c4-abad-f6a9fd3ec49f",
  "status": "pending",
  "status_url": "/jobs/c0fee277-dcd8-44c4-abad-f6a9fd3ec49f"
}
