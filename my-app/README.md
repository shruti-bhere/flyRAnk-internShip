# Assignment 2: Storage Swapping & Containerized Persistence Stack

##  Project Goal
Run Postgres in Docker, connect the application service to it (successfully swapping the volatile in-memory store for a real database repository), and boot the entire app + database stack together seamlessly using a single command.

##  Purpose
This is a core production survival kit applied in one real-world architectural task using **Docker, SQL, and `.env` isolation**. It serves as direct proof of clean layering: proving that switching the underlying storage engine changes **only one configuration file** while keeping core routes and services 100% untouched. Data that survives a hard container restart is the exact moment this project stops being a mere demo and becomes a robust local development stack for future feature updates (caching, jobs, RAG).

---

##  Step-by-Step Execution Guide (How to Start My App)

### 1. Initial Configuration Setup
Before building the containers, ensure your secret runtime credentials are set locally by copying the committed template structure:
```bash
cp .env.example .env
RUN npm install
docker compose up --build

## 2nd terminal 

curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Rahul", "email": "rahul@test.com"}

curl http://localhost:3000/users   


