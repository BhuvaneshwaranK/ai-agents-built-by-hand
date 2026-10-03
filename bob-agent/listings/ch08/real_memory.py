from bob import ChatModel, ModelError, run_agent
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

model = ChatModel("qwen3:4b")
messages = [{"role": "system", "content": SYSTEM_PROMPT}]
try:
    for question in ["Is R-1042 ready?", "And how much will it cost?"]:
        messages.append({"role": "user", "content": question})
        print("Customer:", question)
        print("Bob:   ", run_agent(model, messages, SHOP_TOOLS))
except ModelError as error:
    print("Problem:", error)
