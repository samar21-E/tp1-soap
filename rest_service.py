from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, field_validator
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os
import uvicorn

# Load environment
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "inventory")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "inventory")
DB_NAME = os.getenv("POSTGRES_DB", "inventory")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model
class ProductDB(Base):
    __tablename__ = "products_rest"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class ProductBase(BaseModel):
    name: str
    quantity: int
    price: float
    
    @field_validator('quantity', 'price')
    @classmethod
    def validate_positive(cls, v):
        if v < 0:
            raise ValueError('Value cannot be negative')
        return v

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    
    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(
    title="Inventory REST API",
    description="RESTful API for inventory management",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# REST Endpoints
@app.get("/")
async def root():
    return {"message": "Inventory REST API"}

@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductDB(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(ProductDB).all()

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for field, value in product.model_dump().items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
