from bob import PracticeModel, call_tool, run_agent, say
from bob import shop

notes_path = shop.DATA_DIR / "notes.json"
notes_path.unlink(missing_ok=True)

model = PracticeModel([
    call_tool("remember", note="Amina prefers morning appointments."),
    say("Noted! I will remember that you prefer mornings."),
    call_tool("recall"),
    call_tool("list_free_slots"),
    say("Free morning slots: Mon 10:00, Tue 11:00, and Wed 09:00."),
])
first_visit = [
    {"role": "system", "content": shop.SYSTEM_PROMPT},
    {"role": "user",
     "content": "I'm Amina. I prefer morning appointments."},
]
print("Bob:", run_agent(model, first_visit, shop.SHOP_TOOLS))

second_visit = [
    {"role": "system", "content": shop.SYSTEM_PROMPT},
    {"role": "user", "content": "Hi, it's Amina again. When can I "
                                "come in?"},
]
trace = []
answer = run_agent(model, second_visit, shop.SHOP_TOOLS, trace=trace)
print("Bob:", answer)
print("Recalled:", trace[1]["detail"])
notes_path.unlink()
