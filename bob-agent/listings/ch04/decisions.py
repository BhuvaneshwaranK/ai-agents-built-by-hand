status = "waiting for parts"

if status == "ready for pickup":
    print("Come and collect your bike!")
elif status == "waiting for parts":
    print("We are waiting for a part.")
else:
    print("We are working on it.")

steps = 9
max_steps = 8
if steps > max_steps:
    print("Stop: step limit reached.")
