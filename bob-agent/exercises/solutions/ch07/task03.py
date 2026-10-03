from bob import PracticeModel, call_tool, run_agent, say
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

model = PracticeModel([
    call_tool("check_repair_status", order_id="R-1045"),
    say("Your green child's bike is ready for pickup today. "
        "The price is $20.00."),
])
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user",
     "content": "Is R-1045 ready, and how much will it cost?"},
]
print(run_agent(model, messages, SHOP_TOOLS))
