import textwrap

from bob import PracticeModel, run_agent, say
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

tools = [t for t in SHOP_TOOLS if t["name"] != "search_shop_docs"]
names = ", ".join(t["name"] for t in tools)
print(textwrap.fill("Tools: " + names, 72))

model = PracticeModel([
    say("I'm sorry, I don't know. Please call the shop to ask."),
])
question = "Do you repair electric bikes?"
messages = [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}]
print("Bob:", run_agent(model, messages, tools))
