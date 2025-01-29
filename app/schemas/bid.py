from pydantic import BaseModel
from typing import Optional

class BidCreate(BaseModel):
    product_id: int
    quantity: float
    price_per_kg: float

class BidResponse(BaseModel):
    id: int
    product_id: int
    buyer_id: int
    quantity: float
    price_per_kg: float
    status: str

    class Config:
        from_attributes = True
