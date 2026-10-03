import json
from pathlib import Path


def count_statuses(repairs):
    counts = {}
    for repair in repairs:
        status = repair["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts


text = Path("data/repairs.json").read_text(encoding="utf-8")
counts = count_statuses(json.loads(text))
for status in counts:
    print(status, counts[status])
