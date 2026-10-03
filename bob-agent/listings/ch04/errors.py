import json
from pathlib import Path

repair = {"order_id": "R-1042", "status": "waiting for parts"}

try:
    print(repair["color"])
except KeyError:
    print("That record has no color.")

try:
    data = json.loads("{this is not json")
except json.JSONDecodeError:
    print("That text is not valid JSON.")

try:
    Path("missing_file.txt").read_text(encoding="utf-8")
except FileNotFoundError as error:
    print("Problem:", error)
