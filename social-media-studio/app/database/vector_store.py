from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from app.config import OLLAMA_HOST, EMBED_MODEL, VECTOR_DB_DIR

embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_HOST)

def get_vector_store():
    return Chroma(embedding_function=embeddings, persist_directory=VECTOR_DB_DIR)

def ingest_brand_document(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    return Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=VECTOR_DB_DIR)