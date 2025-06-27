from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import SessionLocal
from ..dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add/{product_id}")
def add_to_cart(product_id: int, quantity: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = models.CartItem(user_id=user.id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    return {"message": "Item added to cart"}


@router.get("/", summary="View my cart items")
def view_cart(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user.id).all()
    return cart_items


@router.delete("/remove/{item_id}", summary="Remove item from cart")
def remove_from_cart(item_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id, models.CartItem.user_id == user.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}


@router.put("/update/{item_id}", summary="Update quantity of cart item")
def update_cart_item_quantity(
    item_id: int,
    new_quantity: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if new_quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

    cart_item.quantity = new_quantity
    db.commit()
    db.refresh(cart_item)

    return {"message": "Cart quantity updated", "cart_item": {
        "id": cart_item.id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity
    }}