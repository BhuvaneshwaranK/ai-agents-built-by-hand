"""Knowledge: let an agent look things up in documents.

This is the simplest honest version of "retrieval": split documents
into small pieces (chunks), score each chunk by how many of the
question's words it contains, and return the best few. Professional
systems often use embeddings instead of word matching, but the shape
of the idea is the same: find, then read.
"""

import re
from pathlib import Path

STOP_WORDS = {
    "a", "an", "and", "are", "can", "do", "does", "for", "how", "i",
    "if", "in", "is", "it", "my", "of", "on", "or", "the", "to", "we",
    "what", "when", "you", "your", "with", "about", "there", "this",
}


def words(text):
    """Lowercase words, minus stop words, with a simple plural rule."""
    found = set()
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        if word in STOP_WORDS:
            continue
        if len(word) > 3 and word.endswith("s"):
            word = word[:-1]
        found.add(word)
    return found


def load_chunks(folder):
    """Split every Markdown file into chunks, one per heading.

    A chunk that is only a heading (such as a document's title) is
    dropped, because it holds nothing a customer could use.
    """
    chunks = []
    for path in sorted(Path(folder).glob("*.md")):
        current = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") and current:
                chunks.append(_chunk(path, current))
                current = []
            current.append(line)
        if current:
            chunks.append(_chunk(path, current))
    return [c for c in chunks if _has_body(c["text"])]


def _has_body(text):
    for line in text.splitlines():
        if line.strip() and not line.startswith("#"):
            return True
    return False


def _chunk(path, lines):
    return {"source": path.name, "text": "\n".join(lines).strip()}


def search(chunks, query, top=3):
    """Return the best-matching chunks, best first."""
    query_words = words(query)
    scored = []
    for chunk in chunks:
        score = len(query_words & words(chunk["text"]))
        if score > 0:
            scored.append({"score": score, "chunk": chunk})
    scored.sort(key=by_score, reverse=True)
    return [item["chunk"] for item in scored[:top]]


def by_score(item):
    return item["score"]
