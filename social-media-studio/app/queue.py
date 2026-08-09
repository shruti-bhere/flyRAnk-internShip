import uuid
from typing import Dict, Any, Optional
from datetime import datetime

JOBS_DB: Dict[str, Dict[str, Any]] = {}

class JobStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

def create_job(topic: str, target_platform: str) -> str:
    job_id = str(uuid.uuid4())
    JOBS_DB[job_id] = {
        "job_id": job_id,
        "topic": topic,
        "target_platform": target_platform,
        "status": JobStatus.PENDING,
        "result": None,
        "error": None,
        "retries": 0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    return job_id

def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    return JOBS_DB.get(job_id)

def update_job(job_id: str, status: str, result: Optional[str] = None, error: Optional[str] = None):
    if job_id in JOBS_DB:
        JOBS_DB[job_id]["status"] = status
        JOBS_DB[job_id]["updated_at"] = datetime.utcnow().isoformat()
        if result is not None:
            JOBS_DB[job_id]["result"] = result
        if error is not None:
            JOBS_DB[job_id]["error"] = error