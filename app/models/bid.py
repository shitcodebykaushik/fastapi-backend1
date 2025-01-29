from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    price_per_kg = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, accepted, rejected

    product = relationship("Product", back_populates="bids")
    buyer = relationship("User", back_populates="bids")
    order = relationship("Order", uselist=False, back_populates="bid")  # Link order
