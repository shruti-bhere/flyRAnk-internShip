# Build Log: Personal RAG Agent (FL-07)

### 1. Core Goal
Build a working personal RAG research agent that ingests unstructured PDFs, generates embeddings, stores them in ChromaDB, and answers queries using Ollama (llama3) with strict grounding.

### 2. Live Tools Connected
- File System & PDF Ingestion (`PyPDFLoader`)
- Local Vector Database (`ChromaDB`)
- Local Inference Engine (`Ollama` with `llama3` and `nomic-embed-text`)

### 3. Challenges & Iterations
- **Issue:** Memory bottlenecks during large document ingestion.
- **Fix:** Used `RecursiveCharacterTextSplitter` with `chunk_size=500` and `chunk_overlap=50`.
- **Issue:** Risk of hallucination on questions out of scope.
- **Fix:** Added strict system prompt guardrail ("Information not found in source documents").

### 4. Spec Deviations
- Used local ChromaDB instead of pgvector for this Checkpoint 1 MVP to keep execution fast and local without additional Docker setup.