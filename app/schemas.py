from pydantic import BaseModel
from datetime import datetime

# Product
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

#user 
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Cart
class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    product: Product

    class Config:
        orm_mode = True


class OrderItem(BaseModel):
    product: Product
    quantity: int

    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    total_price: float
    timestamp: datetime
    items: list[OrderItem]

    class Config:
         orm_mode = True