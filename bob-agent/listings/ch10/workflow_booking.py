from bob import PracticeModel, say, show_trace
from bob import shop
from bob.guardrails import always_allow
from bob.workflows import book_with_workflow

slots_file = shop.DATA_DIR / "slots.json"
original = slots_file.read_text(encoding="utf-8")

model = PracticeModel([
    say("Mon"),
    say("You're booked for gear tuning on Mon 10:00. See you then!"),
])
trace = []
reply = book_with_workflow(
    model, "Can I bring my bike in for gear tuning on Monday?",
    "Tomas", "gear tuning", always_allow, trace)
show_trace(trace)
print("Model calls:", model.calls)
print("Bob:", reply)

slots_file.write_text(original, encoding="utf-8")
