import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from app.schema import GenerationRequest, GenerationResponse
from app.agents.graph import app_graph

app = FastAPI(title="Social Media Studio - Capstone Engine")

@app.post("/generate", response_model=GenerationResponse)
async def generate_content(request: GenerationRequest):
    try:
        initial_state = {
            "topic": request.topic,
            "target_platform": request.target_platform,
            "research_notes": "",
            "draft_content": "",
            "review_status": "PENDING",
            "feedback": "",
            "revision_count": 0
        }
        
        final_state = app_graph.invoke(initial_state)
        
        # --- पोस्ट फाईलमध्ये सेव्ह करण्यासाठीचा कोड ---
        post_data = {
            "timestamp": datetime.now().isoformat(),
            "topic": request.topic,
            "target_platform": request.target_platform,
            "final_post": final_state["draft_content"],
            "revision_count": final_state["revision_count"]
        }
        
        # generated_posts.json मध्ये सेव्ह करणे
        try:
            with open("generated_posts.json", "r") as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []
            
        history.append(post_data)
        
        with open("generated_posts.json", "w") as f:
            json.dump(history, f, indent=4)
        # ---------------------------------------------

        return GenerationResponse(
            topic=request.topic,
            target_platform=request.target_platform,
            final_post=final_state["draft_content"],
            revision_count=final_state["revision_count"],
            review_status=final_state["review_status"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))