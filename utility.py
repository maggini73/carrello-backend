from fastapi import FastAPI
from database import Base, SessionLocal
from models import ProductDB

#Base.metadata.create_all(bind=engine)

def init_products():

    db = next(get_db())

    if db.query(ProductDB).count() == 0:

        products = [
            ProductDB(code="P001", description="Prodotto 1", imageUrl="https://picsum.photos/300/300?random=1", price=10.0),
            ProductDB(code="P002", description="Prodotto 2", imageUrl="https://picsum.photos/300/300?random=2", price=15.5),
            ProductDB(code="P003", description="Prodotto 3", imageUrl="https://picsum.photos/300/300?random=3", price=7.25)
        ]
        db.add_all(products)
        db.commit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 