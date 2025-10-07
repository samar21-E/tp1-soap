from zeep import Client

try:
    client = Client('http://localhost:8000/?wsdl')
    print("Available operations:")
    for service in client.wsdl.services.values():
        print(f"Service: {service.name}")
        for port in service.ports.values():
            print(f"  Port: {port.name}")
            operations = port.binding._operations
            for operation_name in operations:
                print(f"    Operation: {operation_name}")
    
    print("\nTrying to call CreateProduct...")
    result = client.service.CreateProduct("Test", 10, 99.99)
    print(f"Result: {result}")
    
except Exception as e:
    print(f"Error: {e}")
