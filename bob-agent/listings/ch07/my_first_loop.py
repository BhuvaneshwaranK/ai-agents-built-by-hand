from bob import PracticeModel, call_tool, run_tool_call, say
from bob import tool_schemas
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT


def simple_loop(model, messages, tools):
    schemas = tool_schemas(tools)
    while True:
        reply = model.chat(messages, schemas)
        messages.append(reply)
        tool_calls = reply.get("tool_calls") or []
        if not tool_calls:
            return reply["content"]
        for call in tool_calls:
            print("  running", call["function"]["name"])
            result = run_tool_call(call, tools)
            messages.append({"role": "tool",
                             "tool_call_id": call["id"],
                             "content": result})


model = PracticeModel([
    call_tool("calculate_quote",
              services=["brake adjustment", "gear tuning"]),
    call_tool("list_free_slots"),
    say("Together they cost $60.00. Monday has free slots."),
])
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user",
     "content": "How much for a brake adjustment and a gear tuning, "
                "and can you do Monday?"},
]
print("Bob:", simple_loop(model, messages, SHOP_TOOLS))
