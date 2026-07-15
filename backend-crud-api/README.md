# Simple Python FastAPI CRUD API

This is a simple Task Management API (CRUD) built using Python and FastAPI. It runs on a local server and lets you manage a list of tasks.

##  Project Files (How it is organized)
Our project is broken down into small, clean folders:
. `main.py` - The main file that starts our server.
.`routes/` - Holds our URLs and endpoints.
. `controllers/` - Holds the actual logic (how we add, update, or delete tasks).
. `models/` - Sets the rules for our data (using Pydantic).
. `requirements.txt` - A list of libraries we need to install.

---

##  How to Setup and Run

### Step 1: Install the required libraries
Open your terminal inside the project folder and run:
bash
pip install -r requirements.txt
python main.py 

Open in your browser
Home Page: http://127.0.0.1:3000/
Interactive Test Dashboard (Swagger UI): http://127.0.0.1:3000/docs



We used standard status codes to tell the client what happened:

200 OK: Everything worked successfully.

201 Created: A new task was successfully created.

204 No Content: Deletion was successful (no data to return).

400 Bad Request: Client-side error (for example, trying to send an empty task title).

404 Not Found: The task with the requested ID does not exist.