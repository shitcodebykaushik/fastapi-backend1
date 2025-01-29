from pydantic import BaseModel

class OrderCreate(BaseModel):
    bid_id: int  # Buyer selects an accepted bid to confirm

class OrderResponse(BaseModel):
    id: int
    bid_id: int
    buyer_id: int
    farmer_id: int
    product_id: int
    quantity: float
    price_per_kg: float
    total_price: float

    class Config:
        from_attributes = True
