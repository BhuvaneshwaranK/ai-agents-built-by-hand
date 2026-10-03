from bob import ChatModel, ModelError, show_trace
from bob import shop
from bob.tools import ask_in_terminal
from bob.workflows import book_with_workflow

slots_file = shop.DATA_DIR / "slots.json"
original = slots_file.read_text(encoding="utf-8")

model = ChatModel("qwen3:4b")
request = "Can I bring my bike in for gear tuning on Monday?"
trace = []
try:
    reply = book_with_workflow(model, request, "Tomas", "gear tuning",
                               ask_in_terminal, trace)
    show_trace(trace)
    print("Bob:", reply)
except ModelError as error:
    print("Problem:", error)

slots_file.write_text(original, encoding="utf-8")
