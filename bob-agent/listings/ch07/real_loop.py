from bob import ChatModel, ModelError, run_agent, show_trace
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

model = ChatModel("qwen3:4b")
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user",
     "content": "How much for a brake adjustment and a gear tuning, "
                "and can you do Monday?"},
]
trace = []
try:
    answer = run_agent(model, messages, SHOP_TOOLS, trace=trace)
    show_trace(trace)
    print("Model calls:", model.calls,
          "| tokens used:", model.tokens_used)
except ModelError as error:
    print("Problem:", error)
