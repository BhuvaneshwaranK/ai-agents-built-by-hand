from bob import PracticeModel, call_tool, run_tool_call, say
from bob import tool_schemas
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

model = PracticeModel([
    call_tool("check_repair_status", order_id="R-1042"),
    say("It is waiting for a part. It should be ready on Thursday."),
])
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Hi, is R-1042 ready?"},
]

# Call 1: the model sees the tools and asks for one.
reply = model.chat(messages, tool_schemas(SHOP_TOOLS))
messages.append(reply)
call = reply["tool_calls"][0]
print("Model asks for:", call["function"]["name"],
      call["function"]["arguments"])

# Our code runs the tool and adds the result.
result = run_tool_call(call, SHOP_TOOLS)
print("Tool result:", result[:50] + "...")
messages.append({"role": "tool", "tool_call_id": call["id"],
                 "content": result})

# Call 2: the model reads the result and answers.
reply = model.chat(messages, tool_schemas(SHOP_TOOLS))
messages.append(reply)
print("Bob:", reply["content"])
print("Messages:", [m["role"] for m in messages])
