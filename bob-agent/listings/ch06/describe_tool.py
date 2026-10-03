import json

from bob import make_tool, tool_schemas
from bob.shop import check_repair_status

order_tool = make_tool(
    check_repair_status,
    "Look up a repair by its order number, such as R-1042.",
    {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The order number, for example R-1042.",
            },
        },
        "required": ["order_id"],
    },
)
print(order_tool["name"], order_tool["needs_approval"])

schema = tool_schemas([order_tool])[0]
print(schema["type"])
print(schema["function"]["name"])
print(schema["function"]["description"])
print(json.dumps(schema["function"]["parameters"], indent=2))
