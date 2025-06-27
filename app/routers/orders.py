from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import SessionLocal
from ..dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/", summary="View my orders with pagination")
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    orders = db.query(models.Order).filter(models.Order.user_id == user.id).offset(skip).limit(limit).all()
    return orders



@router.post("/place")
def place_order(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = sum(item.quantity * item.product.price for item in cart_items)
    order = models.Order(user_id=user.id, total=total)
    db.add(order)
    db.commit()

    # Clear cart
    db.query(models.CartItem).filter(models.CartItem.user_id == user.id).delete()
    db.commit()

    return {"message": "Order placed", "total": total}
