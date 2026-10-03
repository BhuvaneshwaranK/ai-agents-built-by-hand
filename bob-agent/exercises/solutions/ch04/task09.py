import json
from pathlib import Path

note = {"note": "Call Amina after 5pm"}
Path("practice_note.json").write_text(json.dumps(note),
                                      encoding="utf-8")
saved = json.loads(Path("practice_note.json").read_text(
    encoding="utf-8"))
print(saved["note"])
