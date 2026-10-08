from pathlib import Path

from tree_sitter import Language, Parser
import tree_sitter_python


PYTHON_LANGUAGE = Language(tree_sitter_python.language())

parser = Parser(PYTHON_LANGUAGE)


def chunk_python_file(file_path: str) -> list[dict]:
    """
    Convert a Python file into semantic code chunks.

    Each class and function becomes a separate chunk.
    """

    path = Path(file_path)

    if not path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    if path.suffix.lower() != ".py":
        raise ValueError("Only Python files are supported currently.")

    source_code = path.read_bytes()

    tree = parser.parse(source_code)

    root = tree.root_node

    chunks = []

    for node in root.children:

        if node.type == "function_definition":

            chunks.append(
                create_chunk(
                    node,
                    source_code,
                    path,
                    "function",
                )
            )

        elif node.type == "class_definition":

            chunks.append(
                create_chunk(
                    node,
                    source_code,
                    path,
                    "class",
                )
            )

    return chunks


def create_chunk(
    node,
    source_code: bytes,
    path: Path,
    chunk_type: str,
) -> dict:

    code = source_code[
        node.start_byte:node.end_byte
    ].decode("utf-8")

    name_node = node.child_by_field_name("name")

    if name_node:
        name = source_code[
            name_node.start_byte:name_node.end_byte
        ].decode("utf-8")
    else:
        name = "unknown"

    return {
        "file": str(path),
        "language": "Python",
        "type": chunk_type,
        "name": name,
        "start_line": node.start_point[0] + 1,
        "end_line": node.end_point[0] + 1,
        "code": code,
    }