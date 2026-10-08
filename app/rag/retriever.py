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
    ) -> list[dict]:
        """
        Retrieve the most relevant code chunks for a query.
        """

        query_embedding = self.embedding_model.embed_text(
            query
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
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