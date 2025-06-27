from fastapi import FastAPI
from .import models
from .database import engine
from .routers import products,users,cart,orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(products.router)
app.include_router(users.router)
app.include_router(cart.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI E-commerce!"}

