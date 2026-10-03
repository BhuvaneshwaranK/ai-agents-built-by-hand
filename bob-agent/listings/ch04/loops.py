prices = {"brake adjustment": 25.0, "gear tuning": 35.0}
for service in prices:
    print(service, "costs", prices[service])

total = 0
for service in ["brake adjustment", "gear tuning"]:
    total = total + prices[service]
print("Total:", total)

for step in range(1, 4):
    print("step", step)
