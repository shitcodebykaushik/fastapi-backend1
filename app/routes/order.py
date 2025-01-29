from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.order import Order
from app.models.bid import Bid
from app.models.user import User
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderResponse
from app.utils.auth import get_current_user, require_role

router = APIRouter()

# ✅ Dependency to get the database session
def get_db():
    with Session(engine) as session:
        yield session

# ✅ Buyer confirms a bid to create an order
@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("buyer"))
):
    bid = db.query(Bid).filter(Bid.id == order_data.bid_id, Bid.status == "accepted").first()
    if not bid:
        raise HTTPException(status_code=404, detail="Accepted bid not found")

    # Check if order already exists
    existing_order = db.query(Order).filter(Order.bid_id == bid.id).first()
    if existing_order:
        raise HTTPException(status_code=400, detail="Order already confirmed for this bid")

    total_price = bid.quantity * bid.price_per_kg
    new_order = Order(
        bid_id=bid.id,
        buyer_id=bid.buyer_id,
        farmer_id=bid.product.farmer_id,
        product_id=bid.product_id,
        quantity=bid.quantity,
        price_per_kg=bid.price_per_kg,
        total_price=total_price
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# ✅ Farmer views confirmed orders
@router.get("/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("farmer"))
):
    return db.query(Order).filter(Order.farmer_id == current_user.id).all()
