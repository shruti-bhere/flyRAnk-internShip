import asyncio
import logging
from app.queue import get_job, update_job, JobStatus
from app.agents.graph import app_graph

logger = logging.getLogger("background_worker")

MAX_RETRIES = 3

async def execute_ai_job(job_id: str):
    job = get_job(job_id)
    if not job or job["status"] != JobStatus.PENDING:
        return  # Idempotency check: आधीच चालू किंवा पूर्ण झाले असेल तर थांबवा

    update_job(job_id, status=JobStatus.PROCESSING)

    initial_state = {
        "topic": job["topic"],
        "target_platform": job["target_platform"],
        "research_notes": "",
        "draft_content": "",
        "review_status": "PENDING",
        "feedback": "",
        "revision_count": 0
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Processing job {job_id} (Attempt {attempt}/{MAX_RETRIES})")
            
            # AI एजंटचा heavy कॉल async thread pool मध्ये रन करणे
            final_state = await asyncio.to_thread(app_graph.invoke, initial_state)
            
            update_job(
                job_id, 
                status=JobStatus.COMPLETED, 
                result=final_state["draft_content"]
            )
            logger.info(f"Job {job_id} completed successfully.")
            return

        except Exception as e:
            logger.error(f"Job {job_id} failed on attempt {attempt}: {str(e)}")
            job["retries"] = attempt
            
            if attempt < MAX_RETRIES:
                await asyncio.sleep(2 ** attempt)  # Exponential Backoff
            else:
                update_job(
                    job_id, 
                    status=JobStatus.FAILED, 
                    error=f"Execution failed after {MAX_RETRIES} attempts: {str(e)}"
                )