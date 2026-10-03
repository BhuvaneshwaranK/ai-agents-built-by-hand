from bob import ChatModel, PracticeModel, say

USE_REAL_MODEL = False

if USE_REAL_MODEL:
    model = ChatModel("qwen3:4b")
else:
    model = PracticeModel([say("Hello! I am Bob. How can I help?")])

messages = [
    {"role": "system", "content": "You are Bob, a friendly helper."},
    {"role": "user", "content": "Hello!"},
]
reply = model.chat(messages)
print(reply["content"])
