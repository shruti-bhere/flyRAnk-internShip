from pydantic import BaseModel

# 1. Input schema (Create karta vaparnyasathi)
class TaskCreate(BaseModel):
    title: str

# 2. Output schema (Response dakhvanyasathi) - HA CLASS ASLACH PAIJE
class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool