def total_price(prices, services):
    total = 0
    for service in services:
        total = total + prices[service]
    return total


prices = {"brake adjustment": 25.0, "gear tuning": 35.0}
print(total_price(prices, ["brake adjustment", "gear tuning"]))
