from bob import PracticeModel, call_tool, make_tool, say
from bob import shop
from bob.guardrails import always_deny
from bob_app import handle_message


def opening_hours():
    return "Monday to Saturday, 9:00 to 18:00. Closed on Sundays."


hours_tool = make_tool(opening_hours, "Give the shop's opening hours.",
                       {"type": "object", "properties": {}})
tools = shop.PUBLIC_TOOLS + [hours_tool]

model = PracticeModel([call_tool("opening_hours"),
                       say("We are open Monday to Saturday.")])
messages = [{"role": "system", "content": shop.SYSTEM_PROMPT}]
print(handle_message(model, messages, "When are you open?", tools,
                     always_deny))
print("Tools:", len(shop.PUBLIC_TOOLS), "public +", len(tools) - len(
    shop.PUBLIC_TOOLS), "new")
