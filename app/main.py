from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="RepoPilot",
    description="AI Software Engineer powered by Agentic RAG",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "project": "RepoPilot",
        "status": "running",
        "version": "0.1.0",
    }