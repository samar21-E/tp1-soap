from spyne import Application, rpc, ServiceBase
from spyne.model.primitive import Integer, Unicode, Float
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from sqlalchemy import create_engine, Column, Integer as SqlInteger, String, Float as SqlFloat
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from wsgiref.simple_server import make_server

# Load DB credentials
load_dotenv()
DB_USER = os.getenv("POSTGRES_USER", "inventory")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "inventory")
DB_NAME = os.getenv("POSTGRES_DB", "inventory")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(SqlInteger, primary_key=True, autoincrement=True)
    name = Column(String(100))
    quantity = Column(SqlInteger)
    price = Column(SqlFloat)

Base.metadata.create_all(engine)

class InventoryService(ServiceBase):

    @rpc(Unicode, Integer, Float, _returns=Unicode)
    def CreateProduct(ctx, name, quantity, price):
        if quantity < 0 or price < 0:
            return "Error: Quantity and price cannot be negative"
        session = Session()
        try:
            p = Product(name=name, quantity=quantity, price=price)
            session.add(p)
            session.commit()
            return f"Created product {p.name} with ID {p.id}"
        except Exception as e:
            session.rollback()
            return f"Error creating product: {str(e)}"
        finally:
            session.close()

    @rpc(_returns=Unicode)
    def GetAllProducts(ctx):
        session = Session()
        try:
            products = session.query(Product).all()
            result = "\n".join([f"{p.id} - {p.name} ({p.quantity}x, ${p.price})" for p in products])
            return result or "No products"
        finally:
            session.close()

    @rpc(Integer, _returns=Unicode)
    def GetProduct(ctx, product_id):
        session = Session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                return f"Product: ID={product.id}, Name={product.name}, Quantity={product.quantity}, Price={product.price}"
            else:
                return f"Error: Product with ID {product_id} not found"
        finally:
            session.close()

    @rpc(Integer, Unicode, Integer, Float, _returns=Unicode)
    def UpdateProduct(ctx, product_id, name, quantity, price):
        if quantity < 0 or price < 0:
            return "Error: Quantity and price cannot be negative"
        
        session = Session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                product.name = name
                product.quantity = quantity
                product.price = price
                session.commit()
                return f"Product {product_id} updated successfully"
            else:
                return f"Error: Product with ID {product_id} not found"
        except Exception as e:
            session.rollback()
            return f"Error updating product: {str(e)}"
        finally:
            session.close()

    @rpc(Integer, _returns=Unicode)
    def DeleteProduct(ctx, product_id):
        session = Session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                session.delete(product)
                session.commit()
                return f"Product {product_id} deleted successfully"
            else:
                return f"Error: Product with ID {product_id} not found"
        except Exception as e:
            session.rollback()
            return f"Error deleting product: {str(e)}"
        finally:
            session.close()

# Create SOAP application
application = Application(
    [InventoryService],
    'inventory.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# WSGI application
wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    print("Starting SOAP service on http://localhost:8000")
    print("WSDL available at: http://localhost:8000/?wsdl")
    print("Press Ctrl+C to stop the server")
    
    server = make_server('0.0.0.0', 8000, wsgi_application)
    server.serve_forever()
