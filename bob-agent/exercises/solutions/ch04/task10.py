import json
from pathlib import Path


def find_orders(customer):
    text = Path("data/repairs.json").read_text(encoding="utf-8")
    found = []
    for repair in json.loads(text):
        if repair["customer"].lower() == customer.strip().lower():
            found.append(repair["order_id"])
    return found


print(find_orders("amina"))
print(find_orders("Nobody"))
