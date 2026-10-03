from bob import PracticeModel, call_tool, run_agent, say
from bob.guardrails import always_deny
from bob.shop import SHOP_TOOLS
from bob.workflows import ask_once

by_name = {t["name"]: t for t in SHOP_TOOLS}
SPECIALISTS = {
    "documents": {
        "prompt": "You answer questions from the shop's documents. "
                  "Say which document you used.",
        "tools": [by_name["search_shop_docs"]]},
}
ROUTER_PROMPT = ("Which team should answer? Reply with exactly one "
                 "word: repairs, bookings, documents, or other.")

router = PracticeModel([say("documents")])
expert = PracticeModel([
    call_tool("search_shop_docs", question="open Sundays"),
    say("We are closed on Sundays (hours and location page)."),
])
question = "Are you open on Sundays?"
team = ask_once(router, ROUTER_PROMPT, question).lower()
spec = SPECIALISTS[team]
messages = [{"role": "system", "content": spec["prompt"]},
            {"role": "user", "content": question}]
print(team, "->", run_agent(expert, messages, spec["tools"],
                            approve=always_deny))
