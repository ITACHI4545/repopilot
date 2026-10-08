from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
}


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".go",
    ".rs",
}


def scan_repository(repo_path: str) -> list[dict]:
    """
    Scan a repository and return metadata about supported source files.
    """

    root = Path(repo_path)

    if not root.exists():
        raise ValueError(f"Repository does not exist: {repo_path}")

    if not root.is_dir():
        raise ValueError(f"Repository path is not a directory: {repo_path}")

    files = []

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        if any(directory in IGNORED_DIRECTORIES for directory in path.parts):
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        relative_path = path.relative_to(root)

        files.append(
            {
                "path": str(relative_path),
                "extension": path.suffix.lower(),
                "language": get_language(path.suffix.lower()),
                "size": path.stat().st_size,
            }
        )

    return files


def get_language(extension: str) -> str:
    """
    Convert file extension into a programming language.
    """

    languages = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".h": "C/C++ Header",
        ".hpp": "C++ Header",
        ".go": "Go",
        ".rs": "Rust",
    }

    return languages.get(extension, "Unknown")