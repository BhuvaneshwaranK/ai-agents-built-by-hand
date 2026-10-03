from bob.knowledge import load_chunks

chunks = load_chunks("data/docs")
print(len(chunks), "chunks")
for chunk in chunks:
    first_line = chunk["text"].splitlines()[0]
    print(f"{chunk['source']:24} {first_line}")
