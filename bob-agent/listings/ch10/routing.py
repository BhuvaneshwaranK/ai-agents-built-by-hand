BOOKING_WORDS = ["book", "appointment", "slot", "come in"]


def route(message):
    text = message.lower()
    for word in BOOKING_WORDS:
        if word in text:
            return "booking workflow"
    return "agent"


for message in ["Can I book a slot on Tuesday?",
                "Is R-1042 ready, and how much will it cost?",
                "When can I come in for a full service?",
                "Do you repair electric bikes?",
                "Is my booking for Tuesday still on?"]:
    print(f"{route(message):17} <- {message}")
