import json

from bob import PracticeModel, call_tool, run_agent, say
from bob import shop
from bob.guardrails import always_allow
from bob.workflows import book_with_workflow

slots_file = shop.DATA_DIR / "slots.json"
original = slots_file.read_text(encoding="utf-8")
request = ("Can I bring my bike in on Monday? Actually, Tuesday might "
           "be better. Or Wednesday, whatever is free.")


def bookings():
    return len(json.loads(slots_file.read_text("utf-8"))["booked"])


print("Booked before:", bookings())

# The workflow: the model may only name one day, or NONE.
model = PracticeModel([say("NONE")])
print("Workflow:", book_with_workflow(model, request, "Tomas",
                                      "gear tuning", always_allow))
print("Booked after the workflow:", bookings())

# The agent, with a model that misreads "or" as "and".
model_script = [
    call_tool("book_appointment", slot="Mon 10:00",
              customer_name="Tomas", service="gear tuning"),
    call_tool("book_appointment", slot="Tue 11:00",
              customer_name="Tomas", service="gear tuning"),
    call_tool("book_appointment", slot="Wed 09:00",
              customer_name="Tomas", service="gear tuning"),
    say("All done!"),
]
model = PracticeModel(model_script)
messages = [{"role": "system", "content": shop.SYSTEM_PROMPT},
            {"role": "user", "content": request}]
run_agent(model, messages, shop.SHOP_TOOLS, approve=always_allow)
print("Booked after the agent, approving everything:", bookings())

# The same agent, with an approval rule: one booking per conversation.
slots_file.write_text(original, encoding="utf-8")
approved = []


def one_booking_only(name, arguments):
    if approved:
        return False
    approved.append(arguments["slot"])
    return True


model = PracticeModel(model_script)
run_agent(model, [{"role": "system", "content": shop.SYSTEM_PROMPT},
                  {"role": "user", "content": request}],
          shop.SHOP_TOOLS, approve=one_booking_only)
print("Booked after the agent, one booking only:", bookings())

slots_file.write_text(original, encoding="utf-8")
