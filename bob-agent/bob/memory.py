"""Memory for agents.

Short-term memory is just the list of messages. Models have a limit on
how much text they can read at once (the context window), so long
conversations must be trimmed.

Long-term memory is anything saved outside the conversation, such as
a notes file the agent can write to and read from with tools.
"""

import json
from pathlib import Path


def save_history(messages, path):
    text = json.dumps(messages, indent=2)
    Path(path).write_text(text, encoding="utf-8")


def load_history(path):
    path = Path(path)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def trim_history(messages, keep_last=20):
    """Keep the system message plus about the last keep_last messages.

    The kept part always starts with a "user" message. That keeps each
    tool result next to the assistant message that asked for it (many
    servers reject a tool result without its request), and it gives
    the model a clear place to start reading.
    """
    system = [m for m in messages[:1] if m.get("role") == "system"]
    rest = messages[len(system):]
    if len(rest) <= keep_last:
        return system + rest

    start = len(rest) - keep_last
    while start < len(rest) and rest[start].get("role") != "user":
        start += 1
    if start == len(rest):  # no user message near the end:
        return system + rest  # keep everything rather than lose it
    return system + rest[start:]


class NotesFile:
    """A tiny long-term memory: a JSON list of short notes on disk."""

    def __init__(self, path):
        self.path = Path(path)

    def _load(self):
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def remember(self, note):
        notes = self._load()
        notes.append(note[:200])  # keep notes short on purpose
        text = json.dumps(notes, indent=2)
        self.path.write_text(text, encoding="utf-8")
        return "Saved."

    def recall(self):
        notes = self._load()
        if not notes:
            return "No notes saved yet."
        return "\n".join("- " + n for n in notes)
