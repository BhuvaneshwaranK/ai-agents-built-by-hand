import inspect

from bob import run_agent
from bob.guardrails import MAX_INPUT_CHARACTERS
from bob.shop import PUBLIC_TOOLS, SHOP_TOOLS, SYSTEM_PROMPT


def report(label, ok):
    print(("OK       " if ok else "MISSING  ") + label)


by_name = {t["name"]: t for t in SHOP_TOOLS}
public = [t["name"] for t in PUBLIC_TOOLS]
read_tools = ["check_repair_status", "list_services", "calculate_quote",
              "search_shop_docs", "list_free_slots", "recall"]
missing = [name for name in read_tools if name not in by_name]
steps = inspect.signature(run_agent).parameters["max_steps"].default

report("3  all read tools exist", missing == [])
report("4  booking needs approval",
       by_name["book_appointment"]["needs_approval"])
report("4  notebook tools are staff only",
       "remember" not in public and "recall" not in public)
report(f"5  step limit is 8 (found {steps})", steps == 8)
report(f"5  message limit is 2000 (found {MAX_INPUT_CHARACTERS})",
       MAX_INPUT_CHARACTERS == 2000)
report("6  no refund tool exists", "issue_refund" not in by_name)
report("6  prompt forbids guessing", "Never guess" in SYSTEM_PROMPT)
report("6  prompt treats documents as data",
       "<document>" in SYSTEM_PROMPT)
report("8  shop documents are searchable",
       "search_shop_docs" in by_name)
report("9  refunds go to the owner", "shop owner" in SYSTEM_PROMPT)
report("9  unsure means suggest calling",
       "suggest calling the shop" in SYSTEM_PROMPT)
