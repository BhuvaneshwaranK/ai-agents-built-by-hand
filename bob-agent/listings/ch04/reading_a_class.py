from bob import PracticeModel, say

model = PracticeModel([say("Hello!"), say("Goodbye!")])
print(model.chat([]))
print(model.chat([]))
print("Calls so far:", model.calls)
