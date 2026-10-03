from bob import mcp_sketch


def call(name, arguments):
    request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
               "params": {"name": name, "arguments": arguments}}
    return mcp_sketch.handle_request(request, mcp_sketch.READ_TOOLS)


wrong_argument = call("check_repair_status", {"order": "R-1042"})
print("isError:", wrong_argument["result"]["isError"])
unknown = call("fly", {})
print("error:", unknown["error"]["code"], unknown["error"]["message"])
