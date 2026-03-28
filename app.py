import os
import sys
import argparse
from parser.ast_parser import parse_file
from generator.docstring_generator import generate_docstring
from reports.coverage import generate_coverage_report


def scan_directory(path, style):
    all_functions = []

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                functions, classes = parse_file(file_path)

                print(f"\nFile: {file}")

                for func in functions:
                    if func["docstring"] is None:
                        print(f"Missing docstring: {func['name']}")

                        generated = generate_docstring(func["name"], func["args"], style)
                        print("Suggested Docstring:")
                        print(generated)

                all_functions.extend(functions)

    return all_functions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to project")
    parser.add_argument("--style", default="google", help="Docstring style")

    args = parser.parse_args()

    print("Scanning project...\n")

    functions = scan_directory(args.path, args.style)

    report = generate_coverage_report(functions)

    print("\nCOVERAGE REPORT")
    print(f"Total functions: {report['total']}")
    print(f"With docstrings: {report['with_doc']}")
    print(f"Missing: {report['missing']}")
    print(f"Coverage: {report['coverage']}%")

if __name__ == "__main__":
    main()