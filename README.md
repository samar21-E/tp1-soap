

This project implements an inventory management system using three different architectures:
1. **Monolithic** - Single script with all functionality
2. **SOAP Service** - XML-based web service with WSDL contract
3. **REST Service** - HTTP-based API with JSON

## 📁 Project Structure

```
soap_service/
├── soap_service.py          # SOAP service implementation
├── rest_service.py          # REST service implementation  
├── test_client.py           # SOAP service test client
├── test_rest.py             # REST service test client
├── requirements.txt         # Python dependencies
├── .env                    # Database configuration
└── LAB_ANSWERS.txt         # Lab questions answers
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL (running in Docker)
- Required Python packages

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
Make sure PostgreSQL is running:
```bash
docker ps
```

### 3. Start SOAP Service
```bash
python soap_service.py
```
**Access:** http://localhost:8000/?wsdl

### 4. Start REST Service  
```bash
python rest_service.py
```
**Access:** http://localhost:8001/docs

## 📋 API Documentation

### SOAP Service Endpoints
| Operation | Parameters | Description |
|-----------|------------|-------------|
| `create_product` | `name, quantity, price` | Create new product |
| `get_all_products` | - | Get all products |
| `get_product` | `product_id` | Get product by ID |
| `update_product` | `product_id, name, quantity, price` | Update product |
| `delete_product` | `product_id` | Delete product |

**WSDL URL:** http://localhost:8000/?wsdl

### REST Service Endpoints
| Method | Endpoint | Description | Example Body |
|--------|----------|-------------|--------------|
| `GET` | `/` | API welcome | - |
| `POST` | `/products/` | Create product | `{"name": "Laptop", "quantity": 10, "price": 999.99}` |
| `GET` | `/products/` | Get all products | - |
| `GET` | `/products/{id}` | Get product by ID | - |
| `PUT` | `/products/{id}` | Update product | `{"name": "Gaming Laptop", "quantity": 5, "price": 1299.99}` |
| `DELETE` | `/products/{id}` | Delete product | - |

**OpenAPI Docs:** http://localhost:8001/docs

## 🧪 Testing

### Test SOAP Service
```bash
python test_client.py
```

### Test REST Service
```bash
python test_rest.py
```

### Manual Testing

**SOAP Service:**
```bash
# Check WSDL
curl http://localhost:8000/?wsdl
```

**REST Service:**
```bash
# Create product
curl -X POST "http://localhost:8001/products/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mouse", "quantity": 50, "price": 25.99}'

# Get all products  
curl http://localhost:8001/products/

# Get specific product
curl http://localhost:8001/products/1

# Update product
curl -X PUT "http://localhost:8001/products/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Mouse", "quantity": 25, "price": 35.99}'

# Delete product
curl -X DELETE "http://localhost:8001/products/1"
```

## 🔧 Configuration

### Environment Variables (.env file)
```ini
POSTGRES_USER=inventory
POSTGRES_PASSWORD=inventory  
POSTGRES_DB=inventory
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Database Schema
```sql
products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  quantity INTEGER,
  price FLOAT
)
```

## 📊 Architecture Comparison

| Aspect | Monolithic | SOAP Service | REST Service |
|--------|------------|--------------|--------------|
| **Protocol** | Direct calls | SOAP/XML | HTTP/JSON |
| **Contract** | None | WSDL (strict) | OpenAPI (flexible) |
| **Data Format** | Python objects | XML | JSON |
| **Use Case** | Small apps | Enterprise systems | Web/Mobile apps |

## 🎯 Learning Outcomes

- ✅ Understand limitations of monolithic architecture
- ✅ Implement SOAP services with WSDL contracts  
- ✅ Build RESTful APIs with OpenAPI documentation
- ✅ Connect services to PostgreSQL database
- ✅ Apply input validation and error handling
- ✅ Compare different service architectures

## 📝 Lab Answers

Complete answers to all lab questions are in `LAB_ANSWERS.txt`

## 🆘 Troubleshooting

### Service won't start
- Check if PostgreSQL is running: `docker ps`
- Verify port is available: `netstat -tulpn | grep 8000`
- Check .env file configuration

### Connection refused
- Make sure service is running in another terminal
- Verify correct port number
- Check for error messages in service terminal

### Database errors
- Ensure Docker container is running
- Verify credentials in .env file
- Check database connection with: `python test_db_connection.py`
