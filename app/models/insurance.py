from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Insurance(Base):
    __tablename__ = "insurance"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    coverage = Column(String, nullable=False)
    user_type = Column(String, nullable=False)  # "farmer" or "buyer"

class UserInsurance(Base):
    __tablename__ = "user_insurance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    insurance_id = Column(Integer, ForeignKey("insurance.id"), nullable=False)
    status = Column(String, default="active")  # "active", "claimed", "expired"
    created_at = Column(DateTime, default=datetime.utcnow)
    claimed_at = Column(DateTime, nullable=True)

    user = relationship("User")
    insurance = relationship("Insurance")
