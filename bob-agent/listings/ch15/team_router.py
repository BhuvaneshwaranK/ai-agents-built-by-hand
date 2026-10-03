from bob import PracticeModel, call_tool, run_agent, say
from bob.guardrails import always_deny
from bob.shop import SHOP_TOOLS
from bob.workflows import ask_once

by_name = {t["name"]: t for t in SHOP_TOOLS}
SPECIALISTS = {
    "repairs": {
        "prompt": "You answer questions about repairs and prices at "
                  "The Bike Stop. Use your tools; never guess.",
        "tools": [by_name[n] for n in ["check_repair_status",
                                       "list_services",
                                       "calculate_quote"]]},
    "bookings": {
        "prompt": "You help customers find appointment slots at "
                  "The Bike Stop. Use your tools; never guess.",
        "tools": [by_name[n] for n in ["list_free_slots",
                                       "book_appointment"]]},
}
ROUTER_PROMPT = ("Which team should answer? Reply with exactly one "
                 "word: repairs, bookings, or other.")


def answer(router, specialist_models, question):
    team = ask_once(router, ROUTER_PROMPT, question).lower()
    if team not in SPECIALISTS:
        return "other", "Please call the shop and we will help."
    spec = SPECIALISTS[team]
    messages = [{"role": "system", "content": spec["prompt"]},
                {"role": "user", "content": question}]
    reply = run_agent(specialist_models[team], messages, spec["tools"],
                      approve=always_deny)
    return team, reply


router = PracticeModel([say("repairs"), say("bookings"), say("other")])
specialist_models = {
    "repairs": PracticeModel([
        call_tool("check_repair_status", order_id="R-1045"),
        say("R-1045 is ready for pickup today.")]),
    "bookings": PracticeModel([
        call_tool("list_free_slots"),
        say("Tuesday has a free slot at 11:00.")]),
}
for question in ["Is R-1045 ready?", "Anything free on Tuesday?",
                 "Can you recommend a good bike lock?"]:
    team, reply = answer(router, specialist_models, question)
    print(f"{team:9} {question}")
    print("          " + reply)
print("Model calls: router", router.calls, "| repairs",
      specialist_models["repairs"].calls, "| bookings",
      specialist_models["bookings"].calls)
