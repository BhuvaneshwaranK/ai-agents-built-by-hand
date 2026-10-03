from bob import PracticeModel, call_tool, run_agent, say
from bob.shop import SHOP_TOOLS


def count_tool_calls(trace):
    count = 0
    for event in trace:
        if event["kind"] == "tool_call":
            count = count + 1
    return count


both = call_tool("calculate_quote",
                 services=["brake adjustment", "gear tuning"])
both["tool_calls"] += call_tool("list_free_slots")["tool_calls"]
model = PracticeModel([both, say("Done.")])
trace = []
run_agent(model, [{"role": "user", "content": "Price and slots?"}],
          SHOP_TOOLS, trace=trace)
print(count_tool_calls(trace))
