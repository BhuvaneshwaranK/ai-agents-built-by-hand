import textwrap

from bob import run_tool_call
from bob.shop import SHOP_TOOLS


def make_call(name, arguments):
    return {"id": "test", "type": "function",
            "function": {"name": name, "arguments": arguments}}


tests = [
    make_call("fly_to_the_moon", "{}"),
    make_call("check_repair_status", "{order_id: R-1042"),
    make_call("check_repair_status", '{"order": "R-1042"}'),
    make_call("check_repair_status", '{"order_id": "R-1024"}'),
]
for call in tests:
    print(textwrap.fill(run_tool_call(call, SHOP_TOOLS), 60))
