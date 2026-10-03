BOOKING_WORDS = ["book", "appointment", "slot", "come in"]


def route(message):
    text = message.lower()
    if "refund" in text:
        return "person"
    for word in BOOKING_WORDS:
        if word in text:
            return "booking workflow"
    return "agent"


print(route("I want a refund for my booking"))
print(route("Can I book a slot on Tuesday?"))
print(route("Do you repair electric bikes?"))
