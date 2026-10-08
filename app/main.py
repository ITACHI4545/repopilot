from fastapi import FastAPI

app = FastAPI(
    title="RepoPilot",
    description="AI Software Engineer powered by Agentic RAG",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "project": "RepoPilot",
        "status": "running",
        "version": "0.1.0",
    }