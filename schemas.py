from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    code: str
    description: str
    imageUrl: str
    price: float

class CartItem(BaseModel):
    product_code: str
    quantity: int
    
class OrderRequest(BaseModel):
    items: List[CartItem]

class OrderLine(BaseModel):
    code: str
    quantity: int
    description: str
    price: float

class Order(BaseModel):
    id: str
    created_at: str
    total: float
    lines: List[OrderLine]