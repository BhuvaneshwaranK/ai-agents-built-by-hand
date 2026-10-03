def safe_trim(messages, keep_last):
    first = messages[:1]
    rest = messages[1:]
    if len(rest) <= keep_last:
        return first + rest
    start = len(rest) - keep_last
    while start < len(rest) and rest[start]["role"] != "user":
        start = start + 1
    return first + rest[start:]


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
print([m["role"] for m in safe_trim(messages, 3)])
print([m["role"] for m in safe_trim(messages, 10)])
