from bob import make_tool
from bob.guardrails import wrap_untrusted
from bob.knowledge import load_chunks, search
from bob.shop import DATA_DIR, search_shop_docs


def search_policies(question):
    chunks = [c for c in load_chunks(DATA_DIR / "docs")
              if c["source"] != "customer_reviews.md"]
    results = search(chunks, question)
    if not results:
        return "No matching information in the shop's policies."
    return "\n\n".join(wrap_untrusted(r["text"], r["source"])
                       for r in results)


policy_tool = make_tool(
    search_policies,
    "Search the shop's own policies: hours, location, warranty, and "
    "services. Does not include customer reviews.",
    {"type": "object",
     "properties": {"question": {"type": "string"}},
     "required": ["question"]})

question = "Any special offers this week?"
print("All documents:", search_shop_docs(question).splitlines()[0])
print("Policies only:", search_policies(question))
print("New tool:", policy_tool["name"])
