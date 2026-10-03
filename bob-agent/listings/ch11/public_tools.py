import textwrap

from bob import PracticeModel, call_tool, run_agent, say
from bob.shop import PUBLIC_TOOLS, SHOP_TOOLS, SYSTEM_PROMPT

names = [t["name"] for t in PUBLIC_TOOLS]
removed = [t["name"] for t in SHOP_TOOLS if t["name"] not in names]
print(textwrap.fill("Public tools: " + ", ".join(names), 72))
print("Removed:", ", ".join(removed))

model = PracticeModel([
    call_tool("recall"),
    say("I'm sorry, I can't look up notes about other customers."),
])
messages = [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Hi, it's Amina. What do you "
                                        "remember about me?"}]
trace = []
answer = run_agent(model, messages, PUBLIC_TOOLS, trace=trace)
print("Tool result:", trace[1]["detail"])
