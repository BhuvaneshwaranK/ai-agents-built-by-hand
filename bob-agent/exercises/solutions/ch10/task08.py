import re

from bob import PracticeModel, say
from bob.shop import check_repair_status
from bob.workflows import ask_once

ORDER_PROMPT = ("Reply with only the order number in the message, "
                "such as R-1042, or NONE.")


def status_with_workflow(model, message):
    order_id = ask_once(model, ORDER_PROMPT, message).upper()
    if not re.fullmatch(r"R-\d{4}", order_id):
        return "Please tell me your order number, such as R-1042."
    result = check_repair_status(order_id)
    if isinstance(result, str):
        return result
    return f"{result['bike']}: {result['status']}."


model = PracticeModel([say("r-1043"), say("NONE")])
print(status_with_workflow(model, "Hi, is r-1043 done yet?"))
print(status_with_workflow(model, "Is my bike ready?"))
