import textwrap

from bob import PracticeModel, call_tool, run_agent, say
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

model = PracticeModel([
    call_tool("search_shop_docs",
              question="Do you repair electric bikes?"),
    say("Yes, we repair the mechanical parts of electric bikes, such "
        "as brakes, gears, and tires, but not batteries or motors. "
        "(Source: our services FAQ.)"),
])
question = "Do you repair electric bikes?"
messages = [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}]
trace = []
answer = run_agent(model, messages, SHOP_TOOLS, trace=trace)
for event in trace:
    first_line = event["detail"].splitlines()[0]
    print(event["step"], event["kind"], first_line[:44])
print()
print(textwrap.fill("Bob: " + answer, 72))
