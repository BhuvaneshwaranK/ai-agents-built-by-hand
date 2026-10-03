from bob import PracticeModel, say
from bob import shop
from bob.guardrails import always_allow
from bob.workflows import book_with_workflow

slots_file = shop.DATA_DIR / "slots.json"
original = slots_file.read_text(encoding="utf-8")

model = PracticeModel([say("Wed"), say("All set, see you soon!")])
reply = book_with_workflow(model, "Wednesday, please", "Mei",
                           "brake adjustment", always_allow)
print("Bob:", reply)

slots_file.write_text(original, encoding="utf-8")
