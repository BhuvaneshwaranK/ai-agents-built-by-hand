INPUT_PRICE = 1.00   # example only: US dollars per million tokens
OUTPUT_PRICE = 4.00  # example only: US dollars per million tokens


def estimate_cost(input_tokens, output_tokens):
    total = input_tokens * INPUT_PRICE + output_tokens * OUTPUT_PRICE
    return total / 1000000


steps = [
    {"input": 800, "output": 50},
    {"input": 900, "output": 50},
    {"input": 1000, "output": 60},
]
question_cost = 0
for step in steps:
    question_cost = question_cost + estimate_cost(step["input"],
                                                  step["output"])
print(f"One question: ${question_cost:.4f}")
print(f"1,000 questions: ${question_cost * 1000:.2f}")
