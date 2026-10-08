from app.rag.embeddings import CodeEmbeddingModel


def test_embed_text():

    model = CodeEmbeddingModel()

    embedding = model.embed_text(
        "authenticate user using password"
    )

    assert isinstance(embedding, list)

    assert len(embedding) > 0