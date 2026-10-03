from bob import PracticeModel, call_tool, run_tool_call, say
from bob import tool_schemas
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

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
reply = model.chat(messages, tool_schemas(SHOP_TOOLS))
messages.append(reply)
for call in reply.get("tool_calls") or []:
    result = run_tool_call(call, SHOP_TOOLS)
    messages.append({"role": "tool", "tool_call_id": call["id"],
                     "content": result})
reply = model.chat(messages, tool_schemas(SHOP_TOOLS))
print("Bob:", reply["content"])
print("But the model still wanted:",
      reply["tool_calls"][0]["function"]["name"])
