from bob import PracticeModel, call_tool, run_agent, say
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

PLAN_REQUEST = ("Before doing anything, write a short numbered plan "
                "for answering the customer. Do not answer yet.")

model = PracticeModel([
    say("1. Check the status of R-1042.\n"
        "2. Add up the price of a gear tuning.\n"
        "3. Answer both questions."),
    call_tool("check_repair_status", order_id="R-1042"),
    call_tool("calculate_quote", services=["gear tuning"]),
    say("R-1042 is waiting for a part (ready Thursday). A gear tuning "
        "costs $35.00."),
])
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Is R-1042 ready? And what does a "
                                "gear tuning cost?"},
]

plan = model.chat(messages + [{"role": "user",
                               "content": PLAN_REQUEST}])
print("Plan:")
print(plan["content"])
messages.append({"role": "assistant", "content": plan["content"]})

trace = []
answer = run_agent(model, messages, SHOP_TOOLS, trace=trace)
print("Tools used:", [e["detail"].split("(")[0] for e in trace
                      if e["kind"] == "tool_call"])
print("Model calls:", model.calls)
