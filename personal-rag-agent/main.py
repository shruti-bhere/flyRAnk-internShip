import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

# Updated Imports for LangChain 0.3+
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM

# Classic Chains Imports
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(title="Personal RAG Agent - FL-07 Checkpoint 1")

# Initialize Local Models via Ollama
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = OllamaLLM(model="llama3")

VECTOR_DB_DIR = "./chroma_db"
vector_store = Chroma(embedding_function=embeddings, persist_directory=VECTOR_DB_DIR)

system_prompt = (
    "You are a personal AI Research Scout Agent.\n"
    "Answer the user's question using strictly the retrieved context below.\n"
    "If the answer is not present in the context, respond with 'Information not found in source documents'.\n"
    "Do NOT hallucinate or extrapolate facts.\n\n"
    "Context:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"status": "running", "agent": "Personal RAG Agent"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        os.makedirs("./data", exist_ok=True)
        file_path = f"./data/{file.filename}"
        
        with open(file_path, "wb") as f:
            f.write(await file.read())

        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)

        global vector_store
        vector_store = Chroma.from_documents(
            documents=splits, 
            embedding=embeddings, 
            persist_directory=VECTOR_DB_DIR
        )

        return {
            "status": "success", 
            "filename": file.filename, 
            "chunks_indexed": len(splits)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_agent(request: QueryRequest):
    try:
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        response = rag_chain.invoke({"input": request.question})
        return {
            "question": request.question,
            "answer": response["answer"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)