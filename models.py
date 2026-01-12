from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class ProductDB(Base):
    __tablename__ = "products"
    code = Column(String, primary_key=True, index=True)
    description = Column(String)
    imageUrl = Column(String)
    price = Column(Float)

class OrderDB(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    total = Column(Float)
    lines = relationship("OrderLineDB", back_populates="order", cascade="all, delete-orphan")

class OrderLineDB(Base):
    __tablename__ = "order_lines"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.id"))
    code = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    order = relationship("OrderDB", back_populates="lines")
