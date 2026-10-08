from app.ingestion.chunker import chunk_python_file


def test_chunk_python_file():

    chunks = chunk_python_file(
        "tests/sample_code.py"
    )

    assert len(chunks) == 2

    assert chunks[0]["type"] == "class"
    assert chunks[0]["name"] == "UserService"

    assert chunks[1]["type"] == "function"
    assert chunks[1]["name"] == "calculate_score"