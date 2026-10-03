from pathlib import Path

from bob.knowledge import load_chunks, search

folder = Path("practice_docs")
folder.mkdir(exist_ok=True)
(folder / "payment.md").write_text(
    "## How can I pay?\n\nWe accept cash and cards.\n",
    encoding="utf-8")

results = search(load_chunks(folder), "Can I pay by card?")
print(results[0]["text"])

(folder / "payment.md").unlink()
folder.rmdir()
