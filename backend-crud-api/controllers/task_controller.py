from fastapi import HTTPException, status
from models.task_model import TaskCreate

# In-Memory Database Simulation list
tasks_db = [
    {"id": 1, "title": "Learn Client-Server Architecture", "completed": True},
    {"id": 2, "title": "Build CRUD API Assignment", "completed": False}
]

def get_all_tasks():
    return tasks_db

def create_task(task_data: TaskCreate):
    # Validation constraint check logic
    if not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Client Error: 'title' cannot be empty."
        )
    
    new_id = tasks_db[-1]["id"] + 1 if tasks_db else 1
    new_task = {
        "id": new_id,
        "title": task_data.title,
        "completed": False
    }
    tasks_db.append(new_task)
    return new_task

def update_task(task_id: int, task_data: dict):
    for task in tasks_db:
        if task["id"] == task_id:
            if "title" in task_data and task_data["title"] is not None:
                task["title"] = task_data["title"]
            if "completed" in task_data and task_data["completed"] is not None:
                task["completed"] = task_data["completed"]
            return task
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task with ID {task_id} not found."
    )

def delete_task(task_id: int):
    global tasks_db
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return  # 204 response handles text components dynamically
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task with ID {task_id} not found."
    )