def opening_hours():
    return "Open Monday to Saturday, 9:00 to 18:00."


def shop_address():
    return "12 Market Lane, next to the train station."


tools = {"opening_hours": opening_hours, "shop_address": shop_address}
chosen = "shop_address"
print(tools[chosen]())
