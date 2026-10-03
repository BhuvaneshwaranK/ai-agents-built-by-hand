from bob import run_tool_call
from bob.shop import SHOP_TOOLS

call = {"id": "t", "type": "function",
        "function": {"name": "recall", "arguments": "[1, 2]"}}
print(run_tool_call(call, SHOP_TOOLS))
