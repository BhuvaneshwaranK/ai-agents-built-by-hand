"""The agent loop: the heart of every AI agent.

    1. Send the conversation and the tool list to the model.
    2. If the model answers in words, we are done.
    3. If the model asks for tools, run them and add the results
       to the conversation.
    4. Go back to step 1, but never more than max_steps times.
"""

import textwrap

from .tools import ask_in_terminal, run_tool_call, tool_schemas

STEP_LIMIT_MESSAGE = (
    "I could not finish this task within my step limit, so I stopped. "
    "Please try a simpler request or ask a person at the shop."
)


def run_agent(model, messages, tools, max_steps=8,
              approve=ask_in_terminal, trace=None):
    """Run the loop until the model gives a final answer.

    messages is changed in place, so after the call it holds the whole
    conversation, including every tool request and tool result.
    trace, if you pass a list, collects one entry per event so you can
    see (or test) exactly what happened.
    """
    schemas = tool_schemas(tools)

    for step in range(1, max_steps + 1):
        reply = model.chat(messages, schemas)
        messages.append(reply)

        tool_calls = reply.get("tool_calls") or []
        if not tool_calls:
            answer = reply.get("content") or ""
            _record(trace, step, "answer", answer)
            return answer

        for call in tool_calls:
            name = call["function"]["name"]
            arguments = call["function"]["arguments"]
            _record(trace, step, "tool_call", f"{name}({arguments})")

            result = run_tool_call(call, tools, approve)
            _record(trace, step, "tool_result", result)

            messages.append({
                "role": "tool",
                "tool_call_id": call["id"],
                "content": result,
            })

    _record(trace, max_steps, "stopped", "step limit reached")
    return STEP_LIMIT_MESSAGE


def _record(trace, step, kind, detail):
    if trace is not None:
        trace.append({"step": step, "kind": kind, "detail": detail})


def show_trace(trace, width=72):
    """Print a trace in a form that is easy to read."""
    for event in trace:
        prefix = f"step {event['step']}  {event['kind']:<12} "
        room = width - len(prefix)
        lines = textwrap.wrap(event["detail"], room) or [""]
        print(prefix + lines[0])
        for line in lines[1:]:
            print(" " * len(prefix) + line)
