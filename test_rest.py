import requests

BASE_URL = "http://localhost:8001"

def test_rest_api():
    print("Testing REST API...")
    
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print(f"1. Root: {response.json()}")
    
    # Create products
    products = [
        {"name": "Laptop", "quantity": 10, "price": 999.99},
        {"name": "Mouse", "quantity": 50, "price": 25.99},
        {"name": "Keyboard", "quantity": 30, "price": 75.50}
    ]
    
    created_ids = []
    for i, product in enumerate(products, 1):
        response = requests.post(f"{BASE_URL}/products/", json=product)
        result = response.json()
        created_ids.append(result['id'])
        print(f"{i+1}. Create product: {result}")
    
    # Get all products
    response = requests.get(f"{BASE_URL}/products/")
    print(f"\n5. All products: {response.json()}")
    
    # Get specific product
    response = requests.get(f"{BASE_URL}/products/1")
    print(f"6. Get product 1: {response.json()}")
    
    # Update product
    update_data = {"name": "Gaming Laptop", "quantity": 5, "price": 1299.99}
    response = requests.put(f"{BASE_URL}/products/1", json=update_data)
    print(f"7. Update product 1: {response.json()}")
    
    # Delete product
    response = requests.delete(f"{BASE_URL}/products/2")
    print(f"8. Delete product 2: {response.json()}")
    
    # Final state
    response = requests.get(f"{BASE_URL}/products/")
    print(f"9. Final products: {response.json()}")
    
    print("\n✅ REST API tests completed!")

if __name__ == "__main__":
    test_rest_api()
