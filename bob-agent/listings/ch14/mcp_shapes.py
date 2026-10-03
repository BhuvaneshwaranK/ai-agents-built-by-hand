from bob import mcp_sketch
from bob.shop import SHOP_TOOLS

by_name = {t["name"]: t for t in SHOP_TOOLS}
bob_tool = by_name["check_repair_status"]
mcp_tool = mcp_sketch.to_mcp_tool(bob_tool)

print("MCP keys:", list(mcp_tool.keys()))
print("Same schema as in Chapter 6:",
      mcp_tool["inputSchema"] == bob_tool["parameters"])
print("Required:", mcp_tool["inputSchema"]["required"])
