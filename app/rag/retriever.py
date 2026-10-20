
from app.core.repository_identity import get_repository_id
from app.rag.embeddings import CodeEmbeddingModel
from app.rag.vector_store import CodeVectorStore


class CodeRetriever:
    def __init__(self):
        self.embedding_model = CodeEmbeddingModel()
        self.vector_store = CodeVectorStore()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        repository_path: str | None = None,
    ) -> list[dict]:
        """Retrieve relevant chunks, optionally scoped to a repository."""

        query_embedding = self.embedding_model.embed_text(query)

        repository_id = (
            get_repository_id(repository_path)
            if repository_path is not None
            else None
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            repository_id=repository_id,
        )

        retrieved_chunks = []

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            retrieved_chunks.append(
                {
                    "code": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        return retrieved_chunks
