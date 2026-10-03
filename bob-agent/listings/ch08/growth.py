import json

messages = [{"role": "system", "content": "x" * 500}]
total_sent = 0
for turn in range(1, 21):
    messages.append({"role": "user", "content": "q" * 100})
    sent = round(len(json.dumps(messages)) / 4)
    total_sent = total_sent + sent
    messages.append({"role": "assistant", "content": "a" * 300})
    if turn in [1, 5, 10, 20]:
        print(f"Turn {turn:2}: about {sent} tokens sent")
print("Total over 20 turns: about", total_sent, "tokens")
