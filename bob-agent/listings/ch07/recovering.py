from bob import PracticeModel, call_tool, run_agent, say, show_trace
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

model = PracticeModel([
    call_tool("check_repair_status", order_id="R 1043"),
    call_tool("check_repair_status", order_id="R-1043"),
    say("Your red folding bike is being repaired now. It should be "
        "ready tomorrow."),
])
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Is my bike ready? It's R 1043."},
]
trace = []
answer = run_agent(model, messages, SHOP_TOOLS, trace=trace)
show_trace(trace)
