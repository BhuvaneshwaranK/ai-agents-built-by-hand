from bob.models import strip_thinking

reply = ("<think>The customer wants the price. I should use "
         "calculate_quote.</think>\n\nA gear tuning costs $35.00.")
print("Before:", repr(reply[:30]) + "...")
print("After: ", strip_thinking(reply))
print("Plain text is unchanged:", strip_thinking("Hello!"))
