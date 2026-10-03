from bob import PracticeModel, say

model = PracticeModel([
    say("No, we are closed on Sundays."),
    say("Yes, on Saturdays we are open from 9:00 to 18:00."),
])

messages = [
    {"role": "system", "content": "You are Bob, the helper for "
                                  "The Bike Stop, a bicycle shop."},
    {"role": "user", "content": "Are you open on Sundays?"},
]

reply = model.chat(messages)
messages.append(reply)
print("Bob:", reply["content"])

messages.append({"role": "user", "content": "And on Saturdays?"})
reply = model.chat(messages)
messages.append(reply)
print("Bob:", reply["content"])
print("Messages in the conversation:", len(messages))
