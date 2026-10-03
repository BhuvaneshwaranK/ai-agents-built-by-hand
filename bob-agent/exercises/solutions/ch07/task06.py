from bob import PracticeModel, call_tool, run_agent
from bob.shop import SHOP_TOOLS


def repeated_call(trace):
    calls = []
    for event in trace:
        if event["kind"] == "tool_call":
            calls.append(event["detail"])
    for position in range(1, len(calls)):
        if calls[position] == calls[position - 1]:
            return True
    return False


model = PracticeModel([call_tool("list_free_slots")] * 20)
trace = []
run_agent(model, [{"role": "user", "content": "Any free slots?"}],
          SHOP_TOOLS, max_steps=3, trace=trace)
print(repeated_call(trace))
print(repeated_call([]))
