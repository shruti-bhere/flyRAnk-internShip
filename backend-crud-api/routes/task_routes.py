from fastapi import APIRouter, status, Response
from models.task_model import TaskResponse, TaskCreate
from typing import List, Optional
import controllers.task_controller as controller

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.get("/", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def read_tasks():
    return controller.get_all_tasks()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def add_task(task: TaskCreate):
    return controller.create_task(task)

@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def edit_task(task_id: int, title: Optional[str] = None, completed: Optional[bool] = None):
    # Object dynamic extraction payloads
    update_payload = {}
    if title is not None: update_payload["title"] = title
    if completed is not None: update_payload["completed"] = completed
    return controller.update_task(task_id, update_payload)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int):
    controller.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
