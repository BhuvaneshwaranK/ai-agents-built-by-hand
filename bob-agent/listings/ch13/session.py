import json
import textwrap

from bob import PracticeModel, call_tool, say
from bob import shop
from bob.guardrails import always_allow, limit_actions
from bob_app import handle_message

slots_file = shop.DATA_DIR / "slots.json"
original = slots_file.read_text(encoding="utf-8")

model = PracticeModel([
    call_tool("check_repair_status", order_id="R-1043"),
    say("Your red folding bike is being repaired and should be ready "
        "tomorrow."),
    call_tool("calculate_quote",
              services=["brake adjustment", "gear tuning"]),
    say("Together they cost $60.00."),
    call_tool("list_free_slots"),
    call_tool("book_appointment", slot="Mon 10:00",
              customer_name="Priya", service="gear tuning"),
    say("Done: gear tuning for Priya on Monday at 10:00."),
    call_tool("book_appointment", slot="Tue 11:00",
              customer_name="Priya", service="gear tuning"),
    say("I can only make one booking per conversation. Please call "
        "the shop for a second one."),
    call_tool("recall"),
    say("I'm sorry, I can't look up notes about customers."),
])
messages = [{"role": "system", "content": shop.SYSTEM_PROMPT}]
PAD = " " * 5
# One approval rule for the whole conversation. Here, the customer
# says yes to every question; the limit still allows only one booking.
approve = limit_actions(always_allow, max_actions=1)

for text in ["Hi! Is R-1043 ready?",
             "How much are a brake adjustment and a gear tuning?",
             "Can I book a gear tuning on Monday morning? I'm Priya.",
             "Actually, book Tuesday too.",
             "What do you remember about Amina?"]:
    reply = handle_message(model, messages, text, shop.PUBLIC_TOOLS,
                           approve)
    print(textwrap.fill("You: " + text, 72, subsequent_indent=PAD))
    print(textwrap.fill("Bob: " + reply, 72, subsequent_indent=PAD))

booked = json.loads(slots_file.read_text("utf-8"))["booked"]
print("Bookings now in the diary:", len(booked))
print("Messages in the conversation:", len(messages))

slots_file.write_text(original, encoding="utf-8")
