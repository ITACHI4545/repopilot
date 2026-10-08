from fastapi import APIRouter, HTTPException

from app.ingestion.scanner import scan_repository

router = APIRouter()


@router.get("/scan")
async def scan(repo_path: str):
    try:
        files = scan_repository(repo_path)

        return {
            "repository": repo_path,
            "total_files": len(files),
            "files": files,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )