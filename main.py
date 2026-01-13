from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import Base, SessionLocal
from models import OrderDB, OrderLineDB, ProductDB
from schemas import CartItem, Order, OrderLine, OrderRequest, Product
import utility
from typing import cast
import uuid
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import engine, create_engine

app = FastAPI()

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    utility.init_products()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/products", response_model=List[Product])
def get_products():
    db = next(utility.get_db())
    products = db.query(ProductDB).all()
    return [Product(
        code=cast(str,p.code), 
        description=cast(str,p.description), 
        imageUrl=cast(str,p.imageUrl), 
        price=cast(float,p.price)
    ) for p in products]

@app.get("/orders", response_model=List[Order])
def get_orders():
    db = SessionLocal()

    orders_db = db.query(OrderDB).all()
    orders: List[Order] = []

    for order_db in orders_db:
        order_lines: List[OrderLine] = []

        for line_db in order_db.lines:
            order_lines.append(
                OrderLine(
                    code=line_db.code,
                    description=line_db.description,
                    quantity=line_db.quantity,
                    price=line_db.price
                )
            )

        orders.append(
            Order(
                id=cast(str,order_db.id),
                created_at=order_db.created_at.isoformat(),
                total=cast(float,order_db.total),
                lines=order_lines
            )
        )

    db.close()
    return orders


@app.post("/order", response_model=Order)
def create_order(orderReq: OrderRequest):
    db = next(utility.get_db())
    lines = []
    total = 0
    cart_items = orderReq.items

    for item in cart_items:
        product = db.query(ProductDB).filter(ProductDB.code == item.product_code).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_code} not found")
        
        line_total = product.price * item.quantity
        total += line_total

        lines.append(OrderLineDB(
            code=product.code,
            description=product.description,
            quantity=item.quantity,
            price=product.price
        ))

    order_id = str(uuid.uuid4())
    order_db = OrderDB(
        id=order_id,
        created_at=datetime.now(),
        total=total,
        lines=lines
    )

    db.add(order_db)
    db.commit()
    db.refresh(order_db)

    return Order(
        id=cast(str,order_db.id),
        created_at=order_db.created_at.isoformat(),
        total=cast(float,order_db.total),
        lines=[OrderLine(
            code=l.code,
            description=l.description,
            quantity=l.quantity,
            price=l.price
        ) for l in order_db.lines]
    )
