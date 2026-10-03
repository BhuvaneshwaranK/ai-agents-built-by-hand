from bob import PracticeModel, call_tool, make_tool, run_tool_call
from bob import say, tool_schemas


def opening_hours():
    return "Monday to Saturday, 9:00 to 18:00. Closed on Sundays."


hours_tool = make_tool(opening_hours,
                       "Give the shop's opening hours.",
                       {"type": "object", "properties": {}})
tools = [hours_tool]

model = PracticeModel([
    call_tool("opening_hours"),
    say("We are open Monday to Saturday, 9:00 to 18:00."),
])
messages = [{"role": "user", "content": "When are you open?"}]

reply = model.chat(messages, tool_schemas(tools))
messages.append(reply)
call = reply["tool_calls"][0]
result = run_tool_call(call, tools)
print("Tool result:", result)
messages.append({"role": "tool", "tool_call_id": call["id"],
                 "content": result})
reply = model.chat(messages, tool_schemas(tools))
print("Bob:", reply["content"])
