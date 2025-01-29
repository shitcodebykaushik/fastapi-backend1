from fastapi import FastAPI
from app.routes import auth, product, bid

app = FastAPI()

# Include Authentication, Product, and Bidding Routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(bid.router, prefix="/bids", tags=["Bidding"])

@app.get("/")
def read_root():
    return {"message": "FastAPI Backend is Running!"}
