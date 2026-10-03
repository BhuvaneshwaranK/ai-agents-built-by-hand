from pathlib import Path

from bob.memory import load_history, save_history

messages = [
    {"role": "system", "content": "You are Bob."},
    {"role": "user", "content": "Is R-1042 ready?"},
    {"role": "assistant", "content": "It is waiting for a part."},
]
save_history(messages, "conversation_demo.json")
loaded = load_history("conversation_demo.json")
print(loaded == messages, len(loaded))
print(load_history("no_such_file.json"))
Path("conversation_demo.json").unlink()
