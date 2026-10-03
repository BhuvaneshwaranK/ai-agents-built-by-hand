def greet(name):
    return f"Hello, {name}! Welcome to The Bike Stop."


def quote(prices, services, discount=0):
    total = 0
    for service in services:
        total = total + prices[service]
    return total - discount


prices = {"brake adjustment": 25.0, "gear tuning": 35.0}
message = greet("Amina")
print(message)
print(quote(prices, ["brake adjustment", "gear tuning"]))
print(quote(prices, ["gear tuning"], discount=5))
