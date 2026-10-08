import chromadb


class CodeVectorStore:

    def __init__(
        self,
        collection_name: str = "repopilot_code",
    ):
        self.client = chromadb.PersistentClient(
            path="./data/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
    ):

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings."
            )

        ids = [
            f"chunk_{index}"
            for index in range(len(chunks))
        ]

        documents = [
            chunk["code"]
            for chunk in chunks
        ]

        metadatas = [
            {
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
    ):

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )