from app.ingestion.indexer import RepositoryIndexer


def test_index_repository():

    indexer = RepositoryIndexer()

    result = indexer.index_repository(
        "tests"
    )

    assert result["files_indexed"] >= 1

    assert result["chunks_indexed"] >= 1