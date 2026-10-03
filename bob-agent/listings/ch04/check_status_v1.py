import json
from pathlib import Path


def check_repair_status(order_id):
    text = Path("data/repairs.json").read_text(encoding="utf-8")
    repairs = json.loads(text)
    for repair in repairs:
        if repair["order_id"] == order_id:
            return repair["status"]
    return "No repair found."


print(check_repair_status("R-1042"))
print(check_repair_status("r-1042"))
