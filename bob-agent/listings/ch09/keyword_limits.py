from bob.knowledge import load_chunks, search

chunks = load_chunks("data/docs")
questions = ["Can you fix a flat tire?", "Can you mend a puncture?"]
for question in questions:
    results = search(chunks, question)
    print(question)
    if results:
        print("  best:", results[0]["text"].splitlines()[0])
    else:
        print("  nothing found")
