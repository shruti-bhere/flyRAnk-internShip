from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.services.llm_agent import stream_chat_response
import json

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None

@router.post("/stream")
async def chat_with_agent(request: ChatRequest):
    """
    Ingests user messages and yields real-time streaming text segments from Ollama.
    """
    try:
        async def event_generator():
            # stream_chat_response communicates directly with llm_agent services
            async for token in stream_chat_response(request.message, request.conversation_id):
                # Format compliant with standard Server-Sent Events structure
                yield f"data: {json.dumps({'text': token})}\n\n"
        
        return StreamingResponse(event_generator(), media_type="text/event-stream")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI inference pipeline failure: {str(e)}")