from bob import PracticeModel, call_tool, make_tool, run_agent, say
from bob import show_trace
from bob.shop import SHOP_TOOLS

by_name = {t["name"]: t for t in SHOP_TOOLS}


def ask_repairs_expert(question):
    """A whole agent, wrapped as one tool."""
    expert = PracticeModel([
        call_tool("calculate_quote",
                  services=["brake adjustment", "chain replacement"]),
        say("Those two together cost $55.00."),
    ])
    messages = [{"role": "system",
                 "content": "You are the repairs expert. Use tools."},
                {"role": "user", "content": question}]
    return run_agent(expert, messages, [by_name["calculate_quote"]])


expert_tool = make_tool(
    ask_repairs_expert,
    "Ask the repairs expert a question about repair prices.",
    {"type": "object",
     "properties": {"question": {"type": "string"}},
     "required": ["question"]})

main = PracticeModel([
    call_tool("ask_repairs_expert",
              question="Price of brake adjustment plus new chain?"),
    say("The repairs expert says $55.00 for both."),
])
messages = [{"role": "user",
             "content": "What would brakes and a new chain cost?"}]
trace = []
run_agent(main, messages, [expert_tool], trace=trace)
show_trace(trace)
