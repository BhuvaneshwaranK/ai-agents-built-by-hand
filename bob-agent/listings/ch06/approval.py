from bob import call_tool, run_tool_call
from bob.guardrails import always_deny
from bob.shop import SHOP_TOOLS, list_free_slots

reply = call_tool("book_appointment", slot="Mon 10:00",
                  customer_name="Amina", service="brake adjustment")
result = run_tool_call(reply["tool_calls"][0], SHOP_TOOLS,
                       approve=always_deny)
print(result)
print("Mon 10:00 still free:", "Mon 10:00" in list_free_slots())
