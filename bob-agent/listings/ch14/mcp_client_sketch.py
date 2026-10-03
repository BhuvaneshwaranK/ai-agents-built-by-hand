import json
import subprocess
import sys

META = {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientInfo": {"name": "book-client",
                                           "version": "1.0"},
    "io.modelcontextprotocol/clientCapabilities": {},
}

server = subprocess.Popen([sys.executable, "-m", "bob.mcp_sketch"],
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          text=True)


def send(request_id, method, params):
    params["_meta"] = META
    message = {"jsonrpc": "2.0", "id": request_id, "method": method,
               "params": params}
    server.stdin.write(json.dumps(message) + "\n")
    server.stdin.flush()
    return json.loads(server.stdout.readline())


listing = send(1, "tools/list", {})
names = [tool["name"] for tool in listing["result"]["tools"]]
print("Tools offered:", len(names))
print(" ", ", ".join(names[:3]))
print(" ", ", ".join(names[3:]))

reply = send(2, "tools/call", {"name": "check_repair_status",
                               "arguments": {"order_id": "R-1042"}})
text = reply["result"]["content"][0]["text"]
print("Result:", text[:58] + "...")
print("isError:", reply["result"]["isError"])

refused = send(3, "tools/call", {"name": "book_appointment",
                                 "arguments": {}})
print("Booking over MCP:", refused["error"]["code"],
      refused["error"]["message"])

server.stdin.close()
server.wait()
