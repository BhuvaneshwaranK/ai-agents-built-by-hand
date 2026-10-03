import json
from pathlib import Path

text = Path("data/repairs.json").read_text(encoding="utf-8")
print(type(text))
repairs = json.loads(text)
print(type(repairs), len(repairs))
first = repairs[0]
print(first["order_id"], "-", first["status"])

note = {"customer": "Amina", "prefers": "morning slots"}
as_text = json.dumps(note)
print(as_text)
Path("my_note.json").write_text(as_text, encoding="utf-8")
print(Path("my_note.json").read_text(encoding="utf-8"))
