from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.matcher import check_mismatch_guard

app = FastAPI(title="AI Image Matching Engine")

class MatchRequest(BaseModel):
    post_topic: str
    image_subject: str
    similarity_score: float
    confidence: float

@app.get("/")
def home():
    return {"status": "AI Image Matching Engine is running"}

@app.post("/api/v1/match")
def match_image(req: MatchRequest):
    metadata = {"subject": req.image_subject, "confidence": req.confidence}
    result = check_mismatch_guard(req.post_topic, metadata, req.similarity_score)
    
    if not result["approved"]:
        return {
            "status": "REJECTED",
            "reason": result["reason"]
        }
    
    return {
        "status": "MATCHED",
        "reason": result["reason"]
    }