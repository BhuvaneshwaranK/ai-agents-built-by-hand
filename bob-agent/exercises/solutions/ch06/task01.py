import json

find_orders_parameters = {
    "type": "object",
    "properties": {
        "customer": {
            "type": "string",
            "description": "The customer's first name, such as Amina.",
        },
    },
    "required": ["customer"],
}
print(json.dumps(find_orders_parameters["required"]))
