from fastapi import FastAPI
from routes.task_routes import router as task_router

app = FastAPI(
    title="Python FastAPI CRUD System",
    description="Modular Python backend tracking endpoints visually using Swagger documentation frameworks.",
    version="1.0.0"
)

# 1. HA NAVIN ROUTE ITHE ADD KARA (Welcome Message sathi)
@app.get("/")
def read_root():
    return {
        "message": "Welcome to my Python FastAPI CRUD API!",
        "docs_url": "http://127.0.0.1:3000/docs",
        "api_url": "http://127.0.0.1:3000/api/tasks"
    }

# Mounting routing layers to gateway
app.include_router(task_router)

if __name__ == "__main__":
    import uvicorn
    # Local runtime engine trigger configurations mapping
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)