from bob import PracticeModel, call_tool, run_agent, say
from bob.shop import SHOP_TOOLS

model = PracticeModel([
    call_tool("list_services"),
    call_tool("calculate_quote", services=["full service"]),
    say("A full service costs $80.00."),
])
messages = [{"role": "user", "content": "How much is a full service?"}]
trace = []
print(run_agent(model, messages, SHOP_TOOLS, trace=trace))
print([event["kind"] for event in trace])
