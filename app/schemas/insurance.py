from pydantic import BaseModel
from typing import Optional

class InsuranceBase(BaseModel):
    title: str
    description: str
    price: float
    coverage: str
    user_type: str  # "farmer" or "buyer"

class InsuranceCreate(InsuranceBase):
    pass  # Used for creating insurance

class InsuranceResponse(InsuranceBase):
    id: int  # Ensure this matches the database column name

    class Config:
        from_attributes = True  # ✅ Fix: Replace `orm_mode = True` (Deprecated)
