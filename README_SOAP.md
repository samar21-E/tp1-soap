# SOAP Web Service - Inventory Management

## Overview
This is a SOAP-based web service for inventory management, implementing CRUD operations for products.

## Service Details
- **Endpoint**: http://localhost:8000
- **WSDL**: http://localhost:8000/?wsdl
- **Database**: PostgreSQL

## Available Operations

### CreateProduct
- Creates a new product in the inventory
- Parameters: name (string), quantity (int), price (float)
- Validation: Quantity and price cannot be negative

### GetProduct  
- Retrieves a specific product by ID
- Parameters: product_id (int)

### GetAllProducts
- Retrieves all products in the inventory

### UpdateProduct
- Updates an existing product
- Parameters: product_id (int), name (string), quantity (int), price (float)

### DeleteProduct
- Deletes a product by ID
- Parameters: product_id (int)

## Testing
Run the test client:
```bash
python test_client_corrected.py
