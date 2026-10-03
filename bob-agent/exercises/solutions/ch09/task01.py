from bob.knowledge import load_chunks, search

best = search(load_chunks("data/docs"),
              "How long does a full service take?")[0]
print(best["source"], "|", best["text"].splitlines()[0])
