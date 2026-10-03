messages = [
    {"role": "system", "content": "You are Bob."},
    {"role": "user", "content": "Is R-1042 ready?"},
]
messages.append({"role": "assistant", "content": "Let me check."})
print(len(messages))
print(messages[1]["content"])
print(messages[-1]["role"])
