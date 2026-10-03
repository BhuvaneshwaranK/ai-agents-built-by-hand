# Example prices only. Check your provider's current price list.
PRICE_PER_MILLION_INPUT = 1.00   # US dollars per million input tokens
PRICE_PER_MILLION_OUTPUT = 5.00  # US dollars per million output tokens

questions_per_day = 200
model_calls_per_question = 3     # from your evaluation (Chapter 12)
input_tokens_per_call = 2000     # tools + instructions + history
output_tokens_per_call = 100

calls = questions_per_day * 30 * model_calls_per_question
input_cost = calls * input_tokens_per_call / 1_000_000 * \
    PRICE_PER_MILLION_INPUT
output_cost = calls * output_tokens_per_call / 1_000_000 * \
    PRICE_PER_MILLION_OUTPUT
print(f"Model calls per month: {calls:,}")
print(f"Input:  ${input_cost:,.2f}")
print(f"Output: ${output_cost:,.2f}")
print(f"Total:  ${input_cost + output_cost:,.2f} per month")
