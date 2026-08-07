# To-Do API with SQLite Persistence

A RESTful To-Do API built for Week 2 Part 2 (Connecting CRUD to the database). This project replaces an in-memory storage array with a persistent **SQLite database** while keeping the exact same API endpoints intact.

---

## 📁 What Is Inside This Project?

```text
my-todo-app/
├── main.py           # FastAPI server & SQLite database logic (Python Track)
├── server.js         # Express server & SQLite database logic (Node.js Track)
├── tasks.db          # SQLite database file (created automatically on boot)
├── db-screenshot.png  # Screenshot of DB structure for assignment submission
├── .gitignore        # Prevents node_modules, cache, and DB files from being committed
└── README.md         # Complete project documentation


# 1. Install dependencies
pip install fastapi uvicorn pydantic

# 2. Start the development server
uvicorn main:app --reload



Testing CRUD Endpoints
# Create a new task (Stage 2)
curl -X POST [http://127.0.0.1:8000/tasks](http://127.0.0.1:8000/tasks) \
  -H "Content-Type: application/json" \
  -d '{"title": "Persistent Database Task"}'

# Update task status (Stage 3)
curl -X PUT [http://127.0.0.1:8000/tasks/1](http://127.0.0.1:8000/tasks/1) \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete a task (Stage 3)
curl -X DELETE [http://127.0.0.1:8000/tasks/2](http://127.0.0.1:8000/tasks/2)\