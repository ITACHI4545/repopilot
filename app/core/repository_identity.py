
import hashlib
import os
from pathlib import Path


def get_repository_id(repo_path: str) -> str:
    """Return a stable ID for this repository location."""
    canonical_path = os.path.normcase(
        str(Path(repo_path).resolve())
    )

    digest = hashlib.sha256(
        canonical_path.encode("utf-8")
    ).hexdigest()

    return f"repo_{digest[:24]}"
