
import hashlib

import chromadb


class CodeVectorStore:
    def __init__(
        self,
        collection_name: str = "repopilot_code",
    ):
        self.client = chromadb.PersistentClient(path="./data/chroma")
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    @staticmethod
    def _chunk_id(chunk: dict, repository_id: str) -> str:
        identity = (
            f"{repository_id}:"
            f"{chunk['file']}:"
            f"{chunk['type']}:"
            f"{chunk['name']}:"
            f"{chunk['start_line']}"
        )
        return hashlib.sha256(identity.encode("utf-8")).hexdigest()

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
        repository_id: str = "default",
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings."
            )

        if not chunks:
            return

        ids = [
            self._chunk_id(chunk, repository_id)
            for chunk in chunks
        ]

        documents = [chunk["code"] for chunk in chunks]

        metadatas = [
            {
                "repository_id": repository_id,
                "file": chunk["file"],
                "language": chunk["language"],
                "type": chunk["type"],
                "name": chunk["name"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
            }
            for chunk in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        repository_id: str | None = "default",
    ) -> dict:
        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": min(
                top_k,
                self.collection.count(),
            ),
        }

        if repository_id is not None:
            kwargs["where"] = {"repository_id": repository_id}

        if kwargs["n_results"] == 0:
            return {
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
                "ids": [[]],
            }

        return self.collection.query(**kwargs)
