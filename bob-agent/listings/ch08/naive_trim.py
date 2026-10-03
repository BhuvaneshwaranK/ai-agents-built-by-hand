from bob.memory import trim_history


def naive_trim(messages, keep_last):
    return messages[:1] + messages[-keep_last:]


messages = [
    {"role": "system", "content": "You are Bob."},
    {"role": "user", "content": "Is R-1042 ready?"},
    {"role": "assistant", "content": None,
     "tool_calls": [{"id": "c1"}]},
    {"role": "tool", "tool_call_id": "c1",
     "content": "waiting for parts"},
    {"role": "assistant", "content": "It is waiting for a part."},
    {"role": "user", "content": "When will it be ready?"},
]
print([m["role"] for m in naive_trim(messages, 3)])
print([m["role"] for m in trim_history(messages, keep_last=3)])
