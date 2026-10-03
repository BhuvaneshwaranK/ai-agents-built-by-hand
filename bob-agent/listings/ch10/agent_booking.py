from bob import PracticeModel, call_tool, run_agent, say, show_trace
from bob import shop
from bob.guardrails import always_allow

slots_file = shop.DATA_DIR / "slots.json"
original = slots_file.read_text(encoding="utf-8")

model = PracticeModel([
    call_tool("list_free_slots"),
    call_tool("book_appointment", slot="Mon 10:00",
              customer_name="Tomas", service="gear tuning"),
    say("You're booked for gear tuning on Monday at 10:00."),
])
messages = [
    {"role": "system", "content": shop.SYSTEM_PROMPT},
    {"role": "user", "content": "I'm Tomas. Can I bring my bike in "
                                "for gear tuning on Monday?"},
]
trace = []
run_agent(model, messages, shop.SHOP_TOOLS, approve=always_allow,
          trace=trace)
show_trace(trace)
print("Model calls:", model.calls)

slots_file.write_text(original, encoding="utf-8")
