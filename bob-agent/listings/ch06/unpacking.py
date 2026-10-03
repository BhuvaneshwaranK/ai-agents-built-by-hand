def book(slot, customer_name, service):
    return f"{service} for {customer_name} on {slot}"


arguments = {"slot": "Mon 10:00", "customer_name": "Amina",
             "service": "brake adjustment"}
print(book(**arguments))
print(book(slot="Mon 10:00", customer_name="Amina",
           service="brake adjustment"))
