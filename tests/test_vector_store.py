from app.rag.vector_store import CodeVectorStore


def test_vector_store():

    store = CodeVectorStore(
        collection_name="test_collection"
    )

    chunks = [
        {
            "file": "test.py",
            "language": "Python",
            "type": "function",
            "name": "login",
            "start_line": 1,
            "end_line": 5,
            "code": "def login(): return True",
        }
    ]

    embeddings = [
        [0.1, 0.2, 0.3]
    ]

    store.add_chunks(
        chunks,
        embeddings,
    )

    result = store.search(
        query_embedding=[0.1, 0.2, 0.3],
        top_k=1,
    )

    assert len(result["documents"][0]) == 1

    assert (
        result["documents"][0][0]
        == "def login(): return True"
    )