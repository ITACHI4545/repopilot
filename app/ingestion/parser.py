from pathlib import Path

from tree_sitter import Language, Parser
import tree_sitter_python


PYTHON_LANGUAGE = Language(tree_sitter_python.language())

parser = Parser(PYTHON_LANGUAGE)


def parse_python_file(file_path: str) -> dict:
    """
    Parse a Python file and extract its basic code structure.
    """

    path = Path(file_path)

    if not path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    if path.suffix.lower() != ".py":
        raise ValueError("Only Python files are supported currently.")

    source_code = path.read_bytes()

    tree = parser.parse(source_code)

    root = tree.root_node

    result = {
        "file": str(path),
        "language": "Python",
        "imports": [],
        "functions": [],
        "classes": [],
    }

    for node in root.children:

        if node.type == "import_statement":
            result["imports"].append(
                source_code[node.start_byte:node.end_byte]
                .decode("utf-8")
                .strip()
            )

        elif node.type == "import_from_statement":
            result["imports"].append(
                source_code[node.start_byte:node.end_byte]
                .decode("utf-8")
                .strip()
            )

        elif node.type == "function_definition":

            function_name = get_node_name(node, source_code)

            result["functions"].append(
                {
                    "name": function_name,
                    "line": node.start_point[0] + 1,
                }
            )

        elif node.type == "class_definition":

            class_name = get_node_name(node, source_code)

            methods = []

            body = node.child_by_field_name("body")

            if body:
                for child in body.children:

                    if child.type == "function_definition":
                        method_name = get_node_name(
                            child,
                            source_code
                        )

                        methods.append(
                            {
                                "name": method_name,
                                "line": child.start_point[0] + 1,
                            }
                        )

            result["classes"].append(
                {
                    "name": class_name,
                    "line": node.start_point[0] + 1,
                    "methods": methods,
                }
            )

    return result


def get_node_name(node, source_code: bytes) -> str:
    """
    Extract the identifier/name associated with a class or function.
    """

    name_node = node.child_by_field_name("name")

    if name_node is None:
        return "unknown"

    return source_code[
        name_node.start_byte:name_node.end_byte
    ].decode("utf-8")