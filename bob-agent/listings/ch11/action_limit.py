from bob.guardrails import always_allow, limit_actions

approve = limit_actions(always_allow, max_actions=1)
for slot in ["Mon 10:00", "Tue 11:00", "Wed 09:00"]:
    allowed = approve("book_appointment", {"slot": slot})
    print(slot, "allowed" if allowed else "refused")
