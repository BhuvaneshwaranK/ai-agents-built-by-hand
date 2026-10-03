prices = {"brake adjustment": 25.0, "gear tuning": 35.0}
try:
    print(prices["paint job"])
except KeyError:
    print("Unknown service")
