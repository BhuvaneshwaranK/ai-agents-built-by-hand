import json
from pathlib import Path

text = Path("data/repairs.json").read_text(encoding="utf-8")
for repair in json.loads(text):
    if repair["status"] == "ready for pickup":
        print(repair["order_id"])
