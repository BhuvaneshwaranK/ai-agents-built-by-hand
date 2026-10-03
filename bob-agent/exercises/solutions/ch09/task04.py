from bob.knowledge import load_chunks, search

SYNONYMS = {"puncture": "flat tire", "mend": "fix"}


def expand(question):
    extra = []
    for word in SYNONYMS:
        if word in question.lower():
            extra.append(SYNONYMS[word])
    return question + " " + " ".join(extra)


question = "Can you mend a puncture?"
print(expand(question))
best = search(load_chunks("data/docs"), expand(question))[0]
print(best["text"].splitlines()[0])
