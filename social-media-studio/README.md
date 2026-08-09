# 🚀 Social Media Studio - Multi-Agent AI Engine

An autonomous, multi-agent content orchestration engine built with **FastAPI**, **LangGraph**, **LangChain**, and local **Ollama** models (`llama3` & `nomic-embed-text`). 

The system automates social media content creation through a collaborative feedback loop consisting of a **Researcher Agent**, a **Writer Agent**, and a **Reviewer Agent**, with integrated persistent caching and maximum-revision guardrails.

---

## 🛠️ Tech Stack & Tools Used

* **Framework & API:** FastAPI, Uvicorn
* **Agent Orchestration:** LangGraph, LangChain Core
* **Local Inference (LLM):** Ollama (`llama3`)
* **Vector Embeddings & Storage:** Ollama Embeddings (`nomic-embed-text`), ChromaDB
* **Containerization:** Docker, Docker Compose
* **Language:** Python 3.10+

---

## ⚙️ How It Works (Agent Workflow)

```text
[ User Request ] 
       │
       ▼
    Researcher ->  Gathers key trends & insights for the target platform

       │
       ▼
  
    Writer  ──> Drafts post using research notes & feedback

       │
       ▼
                  REJECTED (Needs Fixes)
   Reviewer   <--------------------------------
       |                                       |
       │                                       │
       │ APPROVED (or Max Revisions = 3)       │
       ▼                                       |
  [ Final Output ] ◄───────────────────────────┘


# how to start 

python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.tx
docker-compose up --build(optional)
ollama pull llama3  
ollama pull nomic-embed-text
python -m app.main          
uvicorn app.main:app --reload --port 8000
Open http://localhost:8000/docs in browser  