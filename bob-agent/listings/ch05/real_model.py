from bob import ChatModel, ModelError

model = ChatModel("qwen3:4b")
messages = [
    {"role": "system", "content": "You are Bob, the helper for "
                                  "The Bike Stop, a bicycle shop. "
                                  "Answer in one sentence."},
    {"role": "user", "content": "Why should I service my bike?"},
]
try:
    reply = model.chat(messages)
    print("Bob:", reply["content"])
    print("Tokens used:", model.tokens_used)
except ModelError as error:
    print("Problem:", error)
