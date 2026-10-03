repair = {
    "order_id": "R-1042",
    "bike": "Mountain bike, black",
    "status": "waiting for parts",
    "ready_by": "Thursday",
    "quote_usd": 60.0,
}
print(repair["status"])
print(repair.get("color"))
print(repair.get("color", "unknown"))
repair["status"] = "in progress"
repair["mechanic"] = "Lena"
print(repair["status"], "/", repair["mechanic"])
print(list(repair.keys()))
