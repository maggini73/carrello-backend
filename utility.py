from fastapi import FastAPI
from database import Base, SessionLocal
from models import ProductDB

#Base.metadata.create_all(bind=engine)

def init_products():

    db = next(get_db())

    if db.query(ProductDB).count() == 0:

        products = [
            ProductDB(code="P001", description="Prodotto 1", imageUrl="img1.png", price=10.0),
            ProductDB(code="P002", description="Prodotto 2", imageUrl="img2.png", price=15.5),
            ProductDB(code="P003", description="Prodotto 3", imageUrl="img3.png", price=7.25)
        ]
        db.add_all(products)
        db.commit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 