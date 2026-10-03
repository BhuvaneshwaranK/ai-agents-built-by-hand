"""A teaching sketch of an MCP server for Bob's read tools.

It shows the message shapes of the Model Context Protocol (MCP),
specification revision 2026-07-28, for tools/list and tools/call over
the stdio transport: one JSON-RPC message per line.

This is NOT a complete MCP server. It does not implement
server/discover, protocol version checks, cancellation, subscriptions,
pagination, or authorization, and it has not been tested with an MCP
client. To build a real server, use an official MCP SDK.

Run it with:  python -m bob.mcp_sketch
"""

import json
import sys

from .guardrails import always_deny
from .shop import PUBLIC_TOOLS
from .tools import run_tool_call

# Least privilege: only tools that change nothing. Actions stay in
# Bob, where a person approves them.
READ_TOOLS = [t for t in PUBLIC_TOOLS if not t["needs_approval"]]


def to_mcp_tool(tool):
    """Describe one of Bob's tools in MCP's shape."""
    return {"name": tool["name"],
            "description": tool["description"],
            "inputSchema": tool["parameters"]}


def handle_request(request, tools):
    """Answer one JSON-RPC request with one JSON-RPC response."""
    method = request.get("method")
    params = request.get("params") or {}
    if method == "tools/list":
        return _result(request, {
            "resultType": "complete",
            "tools": [to_mcp_tool(t) for t in tools]})
    if method == "tools/call":
        name = params.get("name")
        if name not in [t["name"] for t in tools]:
            return _error(request, -32602, f"Unknown tool: {name}")
        call = {"id": "mcp", "type": "function",
                "function": {"name": name,
                             "arguments": params.get("arguments")
                             or {}}}
        text = run_tool_call(call, tools, approve=always_deny)
        return _result(request, {
            "resultType": "complete",
            "content": [{"type": "text", "text": text}],
            "isError": text.startswith("Error")})
    return _error(request, -32601, f"Method not found: {method}")


def serve(tools, stdin=sys.stdin, stdout=sys.stdout):
    """Read one JSON-RPC message per line; write one reply per line."""
    for line in stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            response = {"jsonrpc": "2.0", "id": None,
                        "error": {"code": -32700,
                                  "message": "Parse error"}}
        else:
            if "id" not in request:
                continue  # a notification: no reply is sent
            response = handle_request(request, tools)
        stdout.write(json.dumps(response) + "\n")
        stdout.flush()


def _result(request, result):
    return {"jsonrpc": "2.0", "id": request.get("id"), "result": result}


def _error(request, code, message):
    return {"jsonrpc": "2.0", "id": request.get("id"),
            "error": {"code": code, "message": message}}


if __name__ == "__main__":
    serve(READ_TOOLS)
