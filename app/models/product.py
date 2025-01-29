from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    farmer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    farmer = relationship("User", back_populates="products")
    bids = relationship("Bid", back_populates="product", cascade="all, delete")
