import json

from bob import mcp_sketch

META = {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientInfo": {"name": "book-client",
                                           "version": "1.0"},
    "io.modelcontextprotocol/clientCapabilities": {},
}
request = {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
           "params": {"name": "calculate_quote",
                      "arguments": {"services": ["gear tuning"]},
                      "_meta": META}}
response = mcp_sketch.handle_request(request, mcp_sketch.READ_TOOLS)
print(json.dumps(response, indent=2))
print("One line on the wire:", len(json.dumps(response)), "characters")
