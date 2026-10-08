from app.rag.retriever import CodeRetriever


def test_retrieve_code():

    retriever = CodeRetriever()

    results = retriever.retrieve(
        "user login authentication",
        top_k=2,
    )

    assert isinstance(results, list)

    assert len(results) > 0

    assert "code" in results[0]

    assert "metadata" in results[0]