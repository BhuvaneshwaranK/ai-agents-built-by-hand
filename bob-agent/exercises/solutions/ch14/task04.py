from bob import mcp_sketch
from bob.shop import SHOP_TOOLS
from bob.tools import tool_schemas


def from_mcp_tool(mcp_tool):
    return {"type": "function",
            "function": {"name": mcp_tool["name"],
                         "description": mcp_tool.get("description", ""),
                         "parameters": mcp_tool["inputSchema"]}}


bob_tool = SHOP_TOOLS[0]
round_trip = from_mcp_tool(mcp_sketch.to_mcp_tool(bob_tool))
print(round_trip == tool_schemas([bob_tool])[0])
