from bob import PracticeModel, say
from bob import shop
from bob.guardrails import always_allow
from bob.workflows import book_with_workflow
from bob_app import handle_message

BOOKING_WORDS = ["book", "appointment", "slot", "come in"]


def is_new_booking(text):
    text = text.lower()
    if "my booking" in text:
        return False  # a question about an existing booking
    for word in BOOKING_WORDS:
        if word in text:
            return True
    return False


def respond(model, messages, text, approve, customer_name, service):
    if is_new_booking(text):
        return book_with_workflow(model, text, customer_name, service,
                                  approve)
    return handle_message(model, messages, text, shop.PUBLIC_TOOLS,
                          approve)


slots_file = shop.DATA_DIR / "slots.json"
original = slots_file.read_text(encoding="utf-8")
model = PracticeModel([say("Mon"), say("Booked Mon 10:00. See you!"),
                       say("We are closed on Sundays.")])
messages = [{"role": "system", "content": shop.SYSTEM_PROMPT}]
for text in ["Can I book a slot on Monday?", "Are you open on Sunday?"]:
    print(respond(model, messages, text, always_allow, "Priya",
                  "gear tuning"))
slots_file.write_text(original, encoding="utf-8")
