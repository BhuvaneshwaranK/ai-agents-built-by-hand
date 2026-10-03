import json
from pathlib import Path


def check_repair_status(order_id):
    text = Path("data/repairs.json").read_text(encoding="utf-8")
    repairs = json.loads(text)
    wanted = order_id.strip().lower()
    for repair in repairs:
        if repair["order_id"].lower() == wanted:
            return {
                "order_id": repair["order_id"],
                "bike": repair["bike"],
                "status": repair["status"],
                "ready_by": repair["ready_by"],
            }
    return f"No repair found with order number {order_id}."


result = check_repair_status("R-1042")
print(result["bike"], "-", result["status"])
print(check_repair_status(" r-1043 ")["status"])
print(check_repair_status("R-9999"))
