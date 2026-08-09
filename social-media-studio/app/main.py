from fastapi import FastAPI, BackgroundTasks, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.queue import create_job, get_job
from app.worker import execute_ai_job

app = FastAPI(title="BE-06 Background Job Engine")

class JobRequest(BaseModel):
    topic: str
    target_platform: str

class JobCreationResponse(BaseModel):
    job_id: str
    status: str
    status_url: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    topic: str
    target_platform: str
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: str
    updated_at: str

@app.get("/")
def root():
    return {"status": "running", "service": "Background Job Engine Active"}

# 1. १ सेकंदात HTTP 202 रिस्पॉन्स देणारा एंडपॉईंट
@app.post("/jobs/generate", status_code=status.HTTP_202_ACCEPTED, response_model=JobCreationResponse)
async def trigger_generation_job(request: JobRequest, background_tasks: BackgroundTasks):
    job_id = create_job(topic=request.topic, target_platform=request.target_platform)
    
    # बॅकग्राउंड वर्करला काम सोपवणे
    background_tasks.add_task(execute_ai_job, job_id)
    
    return JobCreationResponse(
        job_id=job_id,
        status="pending",
        status_url=f"/jobs/{job_id}"
    )

# 2. युझर जॉब पूर्ण झाला की नाही ते पाहण्यासाठी पोलिंग एंडपॉईंट
@app.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def check_job_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    
    return JobStatusResponse(**job)