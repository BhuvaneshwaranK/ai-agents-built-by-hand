from bob import PracticeModel, call_tool, run_agent, say
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

model = PracticeModel([
    call_tool("check_repair_status", order_id="R-1042"),
    say("It is waiting for a part. It should be ready on Thursday."),
    say("The agreed price for R-1042 is $60.00."),
])
messages = [{"role": "system", "content": SYSTEM_PROMPT}]
for question in ["Is R-1042 ready?", "And how much will it cost?"]:
    messages.append({"role": "user", "content": question})
    answer = run_agent(model, messages, SHOP_TOOLS)
    print("Customer:", question)
    print("Bob:   ", answer)
roles = [m["role"] for m in messages]
print("Roles:", ", ".join(roles))
