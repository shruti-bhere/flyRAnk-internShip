from fastapi import FastAPI

from app.database import Base, engine

from app.routers import auth
from app.routers import protected

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication Service"
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    protected.router,
    prefix="/user",
    tags=["Protected"]
)


@app.get("/")
def home():

    return {
        "message": "Authentication API Running"
    }