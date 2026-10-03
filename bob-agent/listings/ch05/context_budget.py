import json

from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT
from bob.tools import tool_schemas


def estimate_tokens(text):
    return round(len(text) / 4)


instructions = estimate_tokens(SYSTEM_PROMPT)
tools = estimate_tokens(json.dumps(tool_schemas(SHOP_TOOLS)))
print("Instructions: about", instructions, "tokens")
print("Tool list:    about", tools, "tokens")
print("Sent with every call: about", instructions + tools, "tokens")
print("Share of a 4,096-token window:",
      f"{(instructions + tools) / 4096:.0%}")
