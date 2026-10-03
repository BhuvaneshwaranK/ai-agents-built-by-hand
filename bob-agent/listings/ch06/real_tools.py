from bob import ChatModel, ModelError, run_tool_call, tool_schemas
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

model = ChatModel("qwen3:4b")
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Hi, is R-1042 ready?"},
]
try:
    reply = model.chat(messages, tool_schemas(SHOP_TOOLS))
    messages.append(reply)
    for call in reply.get("tool_calls") or []:
        print("Model asks for:", call["function"]["name"],
              call["function"]["arguments"])
        result = run_tool_call(call, SHOP_TOOLS)
        messages.append({"role": "tool", "tool_call_id": call["id"],
                         "content": result})
    reply = model.chat(messages, tool_schemas(SHOP_TOOLS))
    print("Bob:", reply["content"])
except ModelError as error:
    print("Problem:", error)
