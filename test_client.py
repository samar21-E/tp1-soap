from zeep import Client

def test_soap_service():
    try:
        client = Client('http://localhost:8000/?wsdl')
        
        print("=== Testing SOAP Service ===")
        
        # Test CreateProduct
        print("1. Creating products...")
        result1 = client.service.CreateProduct("Laptop", 10, 999.99)
        print(f"   {result1}")
        
        result2 = client.service.CreateProduct("Mouse", 50, 25.99)
        print(f"   {result2}")
        
        result3 = client.service.CreateProduct("Keyboard", 30, 75.50)
        print(f"   {result3}")
        
        # Test GetAllProducts
        print("\n2. Getting all products...")
        result = client.service.GetAllProducts()
        print(result)
        
        # Test GetProduct
        print("\n3. Getting product with ID 1...")
        result = client.service.GetProduct(1)
        print(f"   {result}")
        
        # Test UpdateProduct
        print("\n4. Updating product with ID 1...")
        result = client.service.UpdateProduct(1, "Gaming Laptop", 5, 1299.99)
        print(f"   {result}")
        
        # Verify update
        print("\n5. Getting updated product...")
        result = client.service.GetProduct(1)
        print(f"   {result}")
        
        # Test DeleteProduct
        print("\n6. Deleting product with ID 2...")
        result = client.service.DeleteProduct(2)
        print(f"   {result}")
        
        # Final state
        print("\n7. Final product list:")
        result = client.service.GetAllProducts()
        print(result)
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_soap_service()
