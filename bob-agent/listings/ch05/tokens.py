from bob.shop import SYSTEM_PROMPT


def estimate_tokens(text):
    return round(len(text) / 4)


question = "Is my bike ready? The order number is R-1042."
print(len(question), "characters, about",
      estimate_tokens(question), "tokens")
print("Bob's instructions: about",
      estimate_tokens(SYSTEM_PROMPT), "tokens")
