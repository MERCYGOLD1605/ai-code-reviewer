def generate_coverage_report(functions):
    total = len(functions)
    with_doc = sum(1 for f in functions if f["docstring"])
    missing = total - with_doc

    coverage = (with_doc / total * 100) if total > 0 else 0

    return {
        "total": total,
        "with_doc": with_doc,
        "missing": missing,
        "coverage": round(coverage, 2)
    }