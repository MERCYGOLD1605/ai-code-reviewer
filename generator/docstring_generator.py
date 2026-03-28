def generate_google(name, args):
    args_section = ""
    if args:
        args_section = "Args:\n"
        for arg in args:
            args_section += f"    {arg}: description\n"

    return f'''"""{name} function.

{args_section}
Returns:
    description
"""'''


def generate_numpy(name, args):
    args_section = ""
    if args:
        args_section = "Parameters\n----------\n"
        for arg in args:
            args_section += f"{arg} : type\n    description\n"

    return f'''"""{name} function.

{args_section}

Returns
-------
type
    description
"""'''


def generate_rest(name, args):
    args_section = ""
    for arg in args:
        args_section += f":param {arg}: description\n"

    return f'''"""{name} function.

{args_section}
:return: description
"""'''


def generate_docstring(name, args, style="google"):
    if style == "numpy":
        return generate_numpy(name, args)
    elif style == "rest":
        return generate_rest(name, args)
    else:
        return generate_google(name, args)