#  Personal RAG & Research Scout Agent (FL-07)

A lightweight, high-performance, and privacy-focused **Retrieval-Augmented Generation (RAG) Agent** built with **FastAPI**, **LangChain**, **ChromaDB**, and **Ollama**. 

This agent dynamic ingestion system processes unstructured PDF documents, chunks and embeds the text into a persistent local vector database, and executes context-grounded Q&A using local Large Language Models with **strict zero-hallucination guardrails**.

---

##  Tech Stack & Tools Used

* **Framework & API:** FastAPI, Uvicorn
* **Orchestration:** LangChain (LangChain Community / Core)
* **Local Inference (LLM):** Ollama (`llama3`)
* **Vector Embeddings:** Ollama Embeddings (`nomic-embed-text`)
* **Vector Database:** ChromaDB (Local persistent storage)
* **Document Parser:** PyPDF
* **Language:** Python 3.10+

---

##  How It Works (Architecture & Workflow)

1. **Document Ingestion (`/upload`):**
   - The user uploads a PDF document via the FastAPI interactive API endpoint.
   - `PyPDFLoader` parses the raw text content from the file.
   - `RecursiveCharacterTextSplitter` divides the document into structured chunks (`chunk_size=500`, `chunk_overlap=50`) to optimize context window efficiency.

2. **Vector Indexing & Storage:**
   - Text chunks are converted into dense vector embeddings locally using `nomic-embed-text`.
   - Embeddings are indexed and stored persistently inside local `./chroma_db`.

3. **Grounded Querying (`/query`):**
   - The user submits a semantic question.
   - ChromaDB retrieves the top $k=3$ most relevant document chunks based on semantic similarity.
   - The retrieved context is passed into `llama3` along with a strict system prompt.

4. **Strict Grounding Guardrail:**
   - The system prompt strictly restricts the LLM from generating answers outside the retrieved payload.
   - If the requested information is absent from the PDF, the agent responds with:
     > *"Information not found in source documents."*

---

##  Step-by-Step Setup & Getting Started

Follow these commands in your terminal to set up and run the application from scratch.

### 1. Clone or Navigate to the Project Folder
```bash
mkdir personal-rag-agent
cd personal-rag-agent

(Mac / Linux:)
python3 -m venv venv. 
source venv/bin/activate

Windows (Command Prompt):
python -m venv venv
venv\Scripts\activate / .\venv\Scripts\Activate.ps1

python main.py 