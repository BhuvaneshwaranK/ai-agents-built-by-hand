from bob.guardrails import always_allow


def deny_names(approve, names):
    def guarded(name, arguments):
        if name in names:
            return False
        return approve(name, arguments)
    return guarded


approve = deny_names(always_allow, ["book_appointment"])
print(approve("book_appointment", {"slot": "Mon 10:00"}))
print(approve("remember", {"note": "Prefers mornings."}))
