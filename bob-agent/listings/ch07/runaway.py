import textwrap

from bob import PracticeModel, call_tool, run_agent
from bob.shop import SHOP_TOOLS

model = PracticeModel([call_tool("list_free_slots")] * 20)
messages = [{"role": "user", "content": "Any free slots?"}]
trace = []
answer = run_agent(model, messages, SHOP_TOOLS, max_steps=3,
                   trace=trace)
for event in trace:
    print(event["step"], event["kind"])
print("Model calls:", model.calls)
print(textwrap.fill(answer, 72))
