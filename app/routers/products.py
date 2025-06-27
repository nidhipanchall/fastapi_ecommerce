from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import SessionLocal
from ..dependencies import get_db, get_current_admin_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

# List products with pagination
@router.get("/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db=db, skip=skip, limit=limit)

# Delete product (admin only)
@router.delete("/{product_id}", summary="Delete a product (admin only)")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin_user)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}


@router.put("/{product_id}", summary="Update a product (admin only)", response_model=schemas.Product)
def update_product(
    product_id: int,
    updated_product: schemas.ProductCreate,  # reuse your create schema
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin_user)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.name = updated_product.name
    product.description = updated_product.description
    product.price = updated_product.price
    product.quantity = updated_product.quantity

    db.commit()
    db.refresh(product)
    return product
