from bob.knowledge import load_chunks, words

question = "Do you repair electric bikes?"
print("Question words:", sorted(words(question)))
for chunk in load_chunks("data/docs"):
    score = len(words(question) & words(chunk["text"]))
    if score > 0:
        first_line = chunk["text"].splitlines()[0]
        print(score, first_line)
