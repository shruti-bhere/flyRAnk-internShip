Date: August 9, 2026

Developer: Shruti Bhere  

Track: Backend AI Engineering  Trigger: Build and debug an interactive PDF processing and query system using dynamic RAG pipelines and vector search.  

Tools Used: Cursor IDE, Claude 3.5 Sonnet, LangChain, LangGraph, LangSmith (for tracing), Hugging Face Embeddings, pg_vector (PostgreSQL).  

Prompts / Inputs:
    "Act as a Backend AI Engineer. Design a dynamic RAG pipeline that accepts any uploaded PDF, extracts text chunks, generates vector embeddings, and performs context-aware semantic search without hardcoded labels.

"Handoffs (Data Flow): Uploaded PDF File -> Text Chunking -> Hugging Face Embeddings -> Store in 
                       pg_vector -> User Query via Streamlit UI -> Vector Search  -> LLM Context Injection -> Output Response. 

Quality Checks & Judgment: 
            Tracing & Debugging: Verified graph state execution and LLM response latency using LangSmith.  

            Accuracy Verification: Checked retrieved context chunks in pg_vector against source PDF pages to prevent hallucinations.  
            
            Code Quality: Tested API endpoints with FastAPI and ensured environment variables (API keys) were secured.  