from sqlalchemy.orm import Session
from . import models, schemas, auth
from .models import Order, OrderItem, CartItem

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not auth.verify_password(password, user.hashed_password):
        return None
    return user

def add_to_cart(db: Session, user_id: int, item: schemas.CartItemCreate):
    cart_item = CartItem(user_id=user_id, product_id=item.product_id, quantity=item.quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def get_user_cart(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()

def remove_cart_item(db: Session, cart_id: int, user_id: int):
    item = db.query(CartItem).filter(CartItem.id == cart_id, CartItem.user_id == user_id).first()
    if item:
        db.delete(item)
        db.commit()
        return True
    return False

