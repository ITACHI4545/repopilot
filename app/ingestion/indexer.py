
from pathlib import Path

from app.core.repository_identity import get_repository_id
from app.ingestion.scanner import scan_repository
from app.ingestion.chunker import chunk_python_file
from app.rag.embeddings import CodeEmbeddingModel
from app.rag.vector_store import CodeVectorStore


class RepositoryIndexer:
    def __init__(self):
        self.embedding_model = CodeEmbeddingModel()
        self.vector_store = CodeVectorStore()

    def index_repository(self, repo_path: str) -> dict:
        root = Path(repo_path).resolve()
        repository_id = get_repository_id(str(root))
        files = scan_repository(str(root))

        total_files = 0
        total_chunks = 0

        for file_info in files:
            if file_info["language"] != "Python":
                continue

            file_path = root / file_info["path"]
            chunks = chunk_python_file(str(file_path))

            if not chunks:
                continue

            # Store relative paths, not machine-specific absolute paths.
            for chunk in chunks:
                chunk["file"] = file_info["path"]

            documents = [chunk["code"] for chunk in chunks]
            embeddings = self.embedding_model.embed_documents(documents)

            self.vector_store.add_chunks(
                chunks=chunks,
                embeddings=embeddings,
                repository_id=repository_id,
            )

            total_files += 1
            total_chunks += len(chunks)

        return {
            "repository": str(root),
            "repository_id": repository_id,
            "files_indexed": total_files,
            "chunks_indexed": total_chunks,
        }
