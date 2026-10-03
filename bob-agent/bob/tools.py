"""Tools: ordinary Python functions that an agent is allowed to use.

The model never runs code itself. It can only *ask* for a tool by
name, with some arguments. Our code decides whether to run it, runs
it, and sends the result back as text.
"""

import json


def make_tool(function, description, parameters, needs_approval=False):
    """Describe a Python function so a model can ask to use it.

    parameters is a JSON Schema object that lists the arguments.
    needs_approval=True means a person must say yes before it runs.
    """
    return {
        "name": function.__name__,
        "function": function,
        "description": description,
        "parameters": parameters,
        "needs_approval": needs_approval,
    }


def tool_schemas(tools):
    """Turn our tool list into the format the model expects to see.

    Notice what is *not* sent: the Python function itself. The model
    only ever sees a name, a description, and the argument rules.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"],
            },
        }
        for t in tools
    ]


def ask_in_terminal(name, arguments):
    """Default approval: ask the person at the keyboard."""
    answer = input(f"\nThe agent wants to run {name}({arguments}). "
                   "Allow? [y/N] ")
    return answer.strip().lower() in ("y", "yes")


def run_tool_call(tool_call, tools, approve=ask_in_terminal):
    """Run one tool call safely and always return text.

    Problems (unknown tool, broken arguments, a crash inside the tool)
    are returned as error messages instead of stopping the program.
    The model reads the message and can try again or explain.
    """
    name = tool_call["function"]["name"]
    by_name = {t["name"]: t for t in tools}

    if name not in by_name:
        return f"Error: there is no tool called '{name}'."

    raw = tool_call["function"]["arguments"] or "{}"
    try:
        arguments = raw if isinstance(raw, dict) else json.loads(raw)
    except json.JSONDecodeError:
        return "Error: the tool arguments were not valid JSON."
    if not isinstance(arguments, dict):
        return "Error: the tool arguments must be a JSON object."

    tool = by_name[name]
    if tool["needs_approval"] and not approve(name, arguments):
        return "The user did not allow this action. Do not retry it."

    try:
        result = tool["function"](**arguments)
    except TypeError as error:
        return f"Error: wrong arguments for {name}: {error}"
    except Exception as error:  # a tool failed; tell the model why
        return f"Error while running {name}: {error}"

    if isinstance(result, str):
        return result
    return json.dumps(result)
