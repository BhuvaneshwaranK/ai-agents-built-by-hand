import re


def keeps_order_numbers(old_text, summary):
    for number in re.findall(r"R-\d{4}", old_text):
        if number not in summary:
            return False
    return True


old = "user: Is R-1042 ready?\nuser: And R-1043?"
print(keeps_order_numbers(old, "R-1042 and R-1043 are in progress."))
print(keeps_order_numbers(old, "Both bikes are in progress."))
