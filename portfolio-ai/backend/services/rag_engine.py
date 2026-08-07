import os
import logging
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from sqlalchemy import text
from backend.core.config import settings
from backend.database.connection import engine

logger = logging.getLogger("portfolio_backend.rag_engine")

# Load the local vector embedding transformer model architecture
embedding_model = SentenceTransformer(settings.HF_EMBEDDING_MODEL)

def process_and_index_pdf(pdf_path: str):
    """
    Extracts content text from raw PDF files, breaks it into structured chunks, 
    calculates vector embeddings, and stores them inside the pgvector backend.
    """
    if not os.path.exists(pdf_path):
        logger.error(f"Target upload file path not found: {pdf_path}")
        return
        
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        text_content = page.extract_text()
        if text_content:
            full_text += text_content + "\n"
            
    # Apply standard chunk size strategies for optimal LLM context matching
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(full_text)
    
    # Ensure the pgvector data schema is explicitly set up in the active target database
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS document_embeddings (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding VECTOR(384)
            );
        """))
        conn.commit()
        
        # Clear existing entries to prevent duplication when re-uploading the resume
        conn.execute(text("TRUNCATE TABLE document_embeddings;"))
        conn.commit()
        
        # Compute vectors and batch-insert items into the database matrix
        for chunk in chunks:
            vector = embedding_model.encode(chunk).tolist()
            conn.execute(
                text("INSERT INTO document_embeddings (content, embedding) VALUES (:content, cast(:embedding as vector));"),
                {"content": chunk, "embedding": str(vector)}
            )
        conn.commit()
    logger.info(f"Successfully chunked and indexed {len(chunks)} fragments into pgvector database.")

def query_semantic_context(user_query: str, limit: int = 3) -> str:
    """
    Performs cosine similarity distance logic searches inside PostgreSQL 
    using the pgvector extension operator (<=>) to locate matching text.
    """
    # Transform incoming prompt to uniform vector spaces
    query_vector = embedding_model.encode(user_query).tolist()
    
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT content FROM document_embeddings 
                    ORDER BY embedding <=> cast(:query_vector as vector) 
                    LIMIT :limit;
                """),
                {"query_vector": str(query_vector), "limit": limit}
            )
            
            matched_chunks = [row[0] for row in result.fetchall()]
            return "\n---\n".join(matched_chunks) if matched_chunks else "No specific documents context found."
    except Exception as e:
        logger.error(f"Database error during pgvector query routine execution: {str(e)}")
        return "Database execution context failure."