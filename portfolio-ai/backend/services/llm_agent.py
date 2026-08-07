import httpx
import json
import logging
from typing import AsyncGenerator
from backend.core.config import settings
from backend.services.rag_engine import query_semantic_context

logger = logging.getLogger("portfolio_backend.llm_agent")

async def stream_chat_response(message: str, conversation_id: str | None = None) -> AsyncGenerator[str, None]:
    """
    Coordinates semantic document retrieval and streams responses back 
    word-by-word using the local Ollama Llama 3 endpoint.
    """
    # 1. Retrieve highly relevant technical context from the pgvector database
    context_blocks = query_semantic_context(message)
    
    # 2. Construct the system prompt injecting personal background constraints
    system_prompt = (
        "You are an expert AI Assistant representing Shruti Suresh Bhere, a final-year B.Com student specialized in "
        "Generative AI, LangGraph workflows, and advanced backend engineering. Answer questions professionally, accurately, "
        "and concisely using the retrieved document context provided below. If the answer cannot be found in the context, "
        "use your general knowledge about her stack (FastAPI, Python, Node.js, LLMs) to answer appropriately.\n\n"
        f"Retrieved Resume/Portfolio Context:\n{context_blocks}"
    )
    
    # 3. Compile the payload configuration for standard Ollama completions API
    payload = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "stream": True
    }
    
    url = f"{settings.OLLAMA_BASE_URL}/api/chat"
    
    # 4. Open an asynchronous streaming connection to the local model container
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("POST", url, json=payload, timeout=60.0) as response:
                if response.status_code != 200:
                    logger.error(f"Ollama local instance returned error status: {response.status_code}")
                    yield "System Error: Unable to perform inference via Ollama at this moment."
                    return
                
                async for line in response.aiter_lines():
                    if line:
                        parsed_line = json.loads(line)
                        token = parsed_line.get("message", {}).get("content", "")
                        if token:
                            yield token
                            
        except Exception as e:
            logger.error(f"Catastrophic failure in LLM agent stream workflow: {str(e)}")
            yield f"Inference engine failure: {str(e)}"