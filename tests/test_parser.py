from app.ingestion.parser import parse_python_file


def test_parse_python_file():

    result = parse_python_file(
        "tests/sample_code.py"
    )

    assert result["language"] == "Python"

    assert "import os" in result["imports"]

    assert len(result["classes"]) == 1

    assert result["classes"][0]["name"] == "UserService"

    assert len(result["classes"][0]["methods"]) == 2

    assert result["classes"][0]["methods"][0]["name"] == "login"

    assert len(result["functions"]) == 1

    assert result["functions"][0]["name"] == "calculate_score"