import textwrap

from bob import PracticeModel, say
from bob.workflows import ask_once

SUMMARY_PROMPT = ("Summarize this conversation in at most two short "
                  "sentences. Keep order numbers, dates, and prices.")


def summarize_old(model, messages, keep_last=2):
    """Replace older messages with one short summary note."""
    system, old = messages[0], messages[1:-keep_last]
    recent = messages[-keep_last:]
    text = "\n".join(f"{m['role']}: {m['content']}" for m in old)
    summary = ask_once(model, SUMMARY_PROMPT, text)
    note = {"role": "system",
            "content": system["content"]
            + "\nEarlier in this conversation: " + summary}
    return [note] + recent


messages = [
    {"role": "system", "content": "You are Bob."},
    {"role": "user", "content": "Is R-1042 ready?"},
    {"role": "assistant", "content": "It is waiting for a part, "
                                     "ready Thursday."},
    {"role": "user", "content": "How much will it cost?"},
    {"role": "assistant", "content": "The agreed price is $60.00."},
    {"role": "user", "content": "Can I pick it up on Friday?"},
    {"role": "assistant", "content": "Yes, we are open 9:00 to 18:00."},
]
model = PracticeModel([say("The customer's bike R-1042 is waiting for "
                           "a part, ready Thursday, price $60.00.")])
shorter = summarize_old(model, messages)
print("Before:", len(messages), "messages")
print("After: ", len(shorter), "messages")
for m in shorter:
    print(textwrap.fill(f"  {m['role']:9} {m['content']}", 72,
                        subsequent_indent=" " * 12))
