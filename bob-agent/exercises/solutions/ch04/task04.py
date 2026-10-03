def is_ready(status):
    return status == "ready for pickup"


print(is_ready("ready for pickup"))
print(is_ready("in progress"))
