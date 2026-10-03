import json

from bob import call_tool

reply = call_tool("check_repair_status", order_id="R-1042")
print(json.dumps(reply, indent=2))
call = reply["tool_calls"][0]
print(type(call["function"]["arguments"]))
arguments = json.loads(call["function"]["arguments"])
print(arguments["order_id"])
