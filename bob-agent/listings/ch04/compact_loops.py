prices = {"brake adjustment": 25.0, "gear tuning": 35.0,
          "full service": 80.0}

cheap = []
for service in prices:
    if prices[service] < 50:
        cheap.append(service)
print(cheap)

cheap = [s for s in prices if prices[s] < 50]
print(cheap)
