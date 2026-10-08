from app.ingestion.scanner import scan_repository


def test_scan_repository():
    files = scan_repository(".")

    assert isinstance(files, list)