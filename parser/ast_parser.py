import ast


class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []

    def visit_FunctionDef(self, node):
        func_data = {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "docstring": ast.get_docstring(node),
            "lineno": node.lineno,
            "node": node
        }
        self.functions.append(func_data)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        class_data = {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "lineno": node.lineno
        }
        self.classes.append(class_data)
        self.generic_visit(node)


def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    parser = CodeParser()
    parser.visit(tree)

    return parser.functions, parser.classes


def get_function_source(file_path, node):
    with open(file_path, "r") as f:
        lines = f.readlines()

    return "".join(lines[node.lineno - 1: node.end_lineno])