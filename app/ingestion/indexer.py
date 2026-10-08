from pathlib import Path

from app.ingestion.scanner import scan_repository
from app.ingestion.chunker import chunk_python_file
from app.rag.embeddings import CodeEmbeddingModel
from app.rag.vector_store import CodeVectorStore


class RepositoryIndexer:

    def __init__(self):
        self.embedding_model = CodeEmbeddingModel()
        self.vector_store = CodeVectorStore()

    def index_repository(self, repo_path: str) -> dict:
        """
        Scan, chunk, embed and store a repository.
        """

        files = scan_repository(repo_path)

        total_files = 0
        total_chunks = 0

        for file_info in files:

            if file_info["language"] != "Python":
                continue

            file_path = Path(repo_path) / file_info["path"]

            chunks = chunk_python_file(
                str(file_path)
            )

            if not chunks:
                continue

            documents = [
                chunk["code"]
                for chunk in chunks
            ]

            embeddings = self.embedding_model.embed_documents(
                documents
            )

            self.vector_store.add_chunks(
                chunks,
                embeddings,
            )

            total_files += 1
            total_chunks += len(chunks)

        return {
            "repository": repo_path,
            "files_indexed": total_files,
            "chunks_indexed": total_chunks,
        }