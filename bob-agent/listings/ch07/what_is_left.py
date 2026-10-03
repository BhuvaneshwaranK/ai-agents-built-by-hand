import json

from bob import PracticeModel, call_tool, run_agent, say
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

model = PracticeModel([
    call_tool("calculate_quote",
              services=["brake adjustment", "gear tuning"]),
    call_tool("list_free_slots"),
    say("Together they cost $60.00. On Monday we have free slots "
        "at 10:00 and 14:00. Shall I book one for you?"),
])
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user",
     "content": "How much for a brake adjustment and a gear tuning, "
                "and can you do Monday?"},
]
run_agent(model, messages, SHOP_TOOLS)
for message in messages:
    print(message["role"])
print(len(messages), "messages, about",
      round(len(json.dumps(messages)) / 4), "tokens")
