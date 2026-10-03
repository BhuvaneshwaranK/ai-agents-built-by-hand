free_slots = ["Mon 10:00", "Mon 14:00", "Tue 11:00"]
print(free_slots)
print(free_slots[0])
print(free_slots[-1])
print(len(free_slots))
free_slots.append("Wed 09:00")
free_slots.remove("Mon 10:00")
print(free_slots)
print("Tue 11:00" in free_slots)
