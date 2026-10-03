"""Workflows: fixed steps, written in code.

In an agent, the model chooses the steps. In a workflow, you do. The
model is still useful, but only for small, well-defined jobs inside
steps that never change, and your code checks its work in between.
"""

from . import shop

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

DAY_PROMPT = (
    "Which day does the customer want? Reply with exactly one of: "
    "Mon, Tue, Wed, Thu, Fri, Sat, or NONE. Reply NONE if no day is "
    "named or if more than one day is possible. No other words."
)

CONFIRM_PROMPT = (
    "Rewrite this booking confirmation as one short, friendly "
    "sentence for the customer. Keep the day, time, and service "
    "exactly as given."
)


def ask_once(model, instructions, text):
    """One narrow model call: instructions plus one piece of text."""
    messages = [{"role": "system", "content": instructions},
                {"role": "user", "content": text}]
    return (model.chat(messages).get("content") or "").strip()


def requested_day(model, request):
    """Step 1: the model names the day. Code checks the answer."""
    day = ask_once(model, DAY_PROMPT, request)[:3].capitalize()
    if day in DAYS:
        return day
    return None


def book_with_workflow(model, request, customer_name, service,
                       approve, trace=None):
    """Book an appointment in five fixed steps."""
    day = requested_day(model, request)
    _note(trace, 1, "model", f"requested day: {day}")
    if day is None:
        return ("Which day would you like? We are open Monday to "
                "Saturday.")

    free = shop.list_free_slots()
    slots = [s for s in free if s.startswith(day)]
    _note(trace, 2, "code", f"free on {day}: {slots}")
    if not slots:
        return f"Sorry, there are no free slots on {day}."

    proposal = {"slot": slots[0], "customer_name": customer_name,
                "service": service}
    allowed = approve("book_appointment", proposal)
    _note(trace, 3, "person", f"approve {slots[0]}? {allowed}")
    if not allowed:
        return ("I have not booked anything. Would another time "
                "suit you?")

    result = shop.book_appointment(**proposal)
    _note(trace, 4, "code", result)

    reply = ask_once(model, CONFIRM_PROMPT, result)
    if slots[0] not in reply:  # check the model kept the facts
        reply = result
    _note(trace, 5, "model", reply)
    return reply


def _note(trace, step, who, detail):
    if trace is not None:
        trace.append({"step": step, "kind": who, "detail": detail})
