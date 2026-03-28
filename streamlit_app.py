import streamlit as st
import os
import difflib
from ai.reviewer import generate_ai_docstring
from parser.ast_parser import parse_file, get_function_source
from generator.docstring_generator import generate_docstring

if "results" not in st.session_state:
    st.session_state.results = []

st.title("AI Code Reviewer")

folder_path = st.text_input("Enter folder path:", "sample_code")

style = st.selectbox("Select Docstring Style", ["google", "numpy", "rest"])


search_term = st.text_input("Search function")
file_filter = st.text_input("Filter by file")


def insert_docstring(file_path, lineno, docstring):
    with open(file_path, "r") as f:
        lines = f.readlines()

    indent = " " * 4
    doc_lines = [indent + line + "\n" for line in docstring.split("\n")]

    lines.insert(lineno, "".join(doc_lines))

    with open(file_path, "w") as f:
        f.writelines(lines)

def preview_change(file_path, lineno, doc):
    with open(file_path, "r") as f:
        original = f.readlines()

    modified = original.copy()

    indent = " " * 4
    doc_lines = [indent + line + "\n" for line in doc.split("\n")]

    modified.insert(lineno, "".join(doc_lines))

    return "".join(original), "".join(modified)


def get_diff(original, modified):
    return "\n".join(difflib.unified_diff(
        original.splitlines(),
        modified.splitlines(),
        lineterm=""
    ))        

if st.button("Scan Code"):
    results = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                functions, _ = parse_file(file_path)

                for func in functions:
                    if func["docstring"] is None:
                        code_snippet = get_function_source(file_path, func["node"])              
                        doc = generate_ai_docstring(code_snippet)

                        results.append({
                            "file": file,
                            "path": file_path,
                            "function": func["name"],
                            "lineno": func["lineno"],
                            "doc": doc
                        })

    st.session_state.results = results

if "results" in st.session_state:

    for i, res in enumerate(st.session_state.results):

        # ✅ FILTER
        if search_term and search_term.lower() not in res["function"].lower():
            continue

        if file_filter and file_filter.lower() not in res["file"].lower():
            continue

        st.subheader(f"{res['file']} → {res['function']}")

        # ✅ DIFF
        original, modified = preview_change(res["path"], res["lineno"], res["doc"])
        diff = get_diff(original, modified)

        st.code(diff, language="diff")

        col1, col2 = st.columns(2)

        # ✅ ACCEPT
        if col1.button(f"Accept {i}"):
            with open(res["path"], "w") as f:
                f.write(modified)

            st.success(f"Inserted docstring for {res['function']}")

        # ❌ REJECT
        if col2.button(f"Reject {i}"):
            st.warning(f"Skipped {res['function']}")