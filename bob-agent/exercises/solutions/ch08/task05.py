from pathlib import Path

from bob.memory import NotesFile


def notes_for(customer):
    if not customer.isalpha():
        raise ValueError("A customer name may contain letters only.")
    return NotesFile(Path(f"notes_{customer}.json"))


notes = notes_for("Amina")
notes.remember("Prefers morning appointments.")
print(notes.recall())
Path("notes_Amina.json").unlink()

try:
    notes_for("../repairs")
except ValueError as error:
    print("Refused:", error)
