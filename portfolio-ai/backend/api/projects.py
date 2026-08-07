from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.database.models import Project
from backend.services.github import fetch_github_repositories
from pydantic import BaseModel

router = APIRouter()

class ProjectSchema(BaseModel):
    title: str
    description: str
    tech_stack: list[str]
    live_link: str | None = None
    github_link: str | None = None
    category: str

@router.get("/static")
async def get_curated_projects(db: Session = Depends(get_db)):
    """
    Retrieves core project profiles saved in the local SQL database.
    """
    return db.query(Project).all()

@router.get("/github/{username}")
async def get_live_repositories(username: str):
    """
    Fetches real-time repository data, stars, and language breakdowns using the GitHub API.
    """
    try:
        repos = await fetch_github_repositories(username)
        return repos
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to query GitHub API: {str(e)}")