from pydantic import BaseModel

class GenerationRequest(BaseModel):
    topic: str
    target_platform: str  # e.g., "LinkedIn", "X/Twitter"

class GenerationResponse(BaseModel):
    topic: str
    target_platform: str
    final_post: str
    revision_count: int
    review_status: str