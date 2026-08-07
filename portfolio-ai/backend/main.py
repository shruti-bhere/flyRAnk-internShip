import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.database.connection import engine
from backend.database import models
from backend.api import auth, chat, projects, telemetry

# Configure structural application logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
)
logger = logging.getLogger("portfolio_backend")

# Automatically generate database tables on app startup if they do not exist
try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("Database schemas verified and initialized successfully.")
except Exception as e:
    logger.error(f"Critical error during database table initialization: {e}")

# Initialize the central FastAPI application instance
app = FastAPI(
    title="AI Engineer Portfolio & Assistant Platform API",
    description="Backend microservices driving the unified RAG engine, project telemetry, and administrative portal.",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Establish CORS policy allowing secure requests from your frontend layer
origins = [
    "http://localhost:5500",  # Default Live Server port
    "http://127.0.0.1:5500",
    "http://localhost:3000",  # Alternative local development port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount application routing layers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication Layer"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["AI Agent Workspace"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Project Data Layer"])
app.include_router(telemetry.router, prefix="/api/v1/telemetry", tags=["System Metrics Engine"])

@app.get("/health", tags=["System Operations"])
async def health_check():
    """
    Evaluates basic service readiness. Used by Docker healthchecks or system monitoring nodes.
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "live_engine": "Ollama + Llama 3 Stack"
    }