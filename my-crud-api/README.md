# FlyRank Backend Track — Assignment A2: Connecting CRUD to SQLite

This project updates the in-memory CRUD API built in Assignment 1 by connecting its storage layer to a persistent SQLite database (`tasks.db`). The API endpoints, request validation, and status codes remain identical to A1, but data now survives application restarts.

---

## 🛠️ Tech Stack & Database Choice

- **Framework:** FastAPI (Python 3.10+)
- **Database:** SQLite3 (standard Python library)
- **Data Validation:** Pydantic

### Why SQLite?
1. **Zero Configuration:** SQLite is serverless and operates directly from a single local file (`tasks.db`).
2. **Persistence:** Data survives server restarts without needing external database servers (like PostgreSQL or MySQL).
3. **Simplicity:** It requires no external services to install or run, making cloning and setup fast and reliable.

---

## 🚀 How to Run the Application

### 1. Prerequisites
Ensure Python 3.10+ is installed on your machine.

### 2. Setup Virtual Environment & Install Dependencies
```bash
# Clone the repository
git clone [https://github.com/shruti-bhere/my-curd-api.git](https://github.com/shruti-bhere/my-curd-api.git)
cd my-curd-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt