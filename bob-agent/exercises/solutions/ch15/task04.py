PRICE_PER_MILLION_INPUT = 1.00
PRICE_PER_MILLION_OUTPUT = 5.00
calls = 200 * 30 * 5
cost = (calls * 2000 / 1_000_000 * PRICE_PER_MILLION_INPUT
        + calls * 100 / 1_000_000 * PRICE_PER_MILLION_OUTPUT)
print(f"{calls:,} calls, ${cost:,.2f} per month")
