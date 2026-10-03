from bob import PracticeModel, call_tool, run_agent, say
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT


def ask(model, question):
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}]
    answer = run_agent(model, messages, SHOP_TOOLS)
    return answer, messages


model = PracticeModel([
    call_tool("check_repair_status", order_id="R-1042"),
    say("It is waiting for a part. It should be ready on Thursday."),
    say("Which bike do you mean? Please tell me your order number."),
])
answer, sent = ask(model, "Is R-1042 ready?")
print("Bob:", answer)
answer, sent = ask(model, "And how much will it cost?")
print("Bob:", answer)
print("The model saw only:", [m["role"] for m in sent[:-1]])
print("The question was:", sent[1]["content"])
