from bob import PracticeModel, call_tool, run_agent, say, show_trace
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

both = call_tool("calculate_quote",
                 services=["brake adjustment", "gear tuning"])
both["tool_calls"] += call_tool("list_free_slots")["tool_calls"]

model = PracticeModel([
    both,
    say("$60.00 in total, and Monday has slots at 10:00 and 14:00."),
])
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user",
     "content": "How much for a brake adjustment and a gear tuning, "
                "and can you do Monday?"},
]
trace = []
run_agent(model, messages, SHOP_TOOLS, trace=trace)
show_trace(trace)
print("Model calls:", model.calls)
