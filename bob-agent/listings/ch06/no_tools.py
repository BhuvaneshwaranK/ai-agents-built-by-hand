from bob import PracticeModel, say
from bob.shop import check_repair_status

# The practice model plays the part of a model with no tools.
model = PracticeModel([
    say("Yes! Your bike R-1042 is ready for pickup."),
])
messages = [{"role": "user", "content": "Is R-1042 ready?"}]
print("Model says:  ", model.chat(messages)["content"])
print("Records say: ", check_repair_status("R-1042")["status"])
