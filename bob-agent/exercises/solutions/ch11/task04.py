from bob.guardrails import always_deny, limit_actions

approve = limit_actions(always_deny, max_actions=3)
print([approve("book_appointment", {}) for _ in range(4)])
