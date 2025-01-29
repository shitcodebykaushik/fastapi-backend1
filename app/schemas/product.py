from pydantic import BaseModel
from typing import Optional

# ✅ Schema for Farmer Details in Product Response
class FarmerInfo(BaseModel):
    id: int
    full_name: str
    phone: str

# ✅ Schema for Product Response (Includes Farmer Info)
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: float
    image_url: Optional[str] = None
    farmer: FarmerInfo  # ✅ Now includes farmer's name & phone

    class Config:
        from_attributes = True

# ✅ Schema for Creating a New Product (No farmer details needed)
class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: float
    image_url: Optional[str] = None
