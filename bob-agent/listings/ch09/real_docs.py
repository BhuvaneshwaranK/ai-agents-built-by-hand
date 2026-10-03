from bob import ChatModel, ModelError, run_agent, show_trace
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

model = ChatModel("qwen3:4b")
for question in ["Do you repair electric bikes?",
                 "Can you mend a puncture?"]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}]
    trace = []
    try:
        answer = run_agent(model, messages, SHOP_TOOLS, trace=trace)
        show_trace(trace)
    except ModelError as error:
        print("Problem:", error)
