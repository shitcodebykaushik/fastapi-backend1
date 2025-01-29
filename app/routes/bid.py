from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.bid import Bid
from app.models.user import User
from app.models.product import Product
from app.models.notification import Notification
from app.schemas.bid import BidCreate, BidResponse
from app.utils.auth import get_current_user, require_role

router = APIRouter()

# ✅ Dependency to get the database session
def get_db():
    with Session(engine) as session:
        yield session

# ✅ Buyer places a bid on a product
@router.post("/", response_model=BidResponse)
def place_bid(
    bid: BidCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("buyer"))
):
    product = db.query(Product).filter(Product.id == bid.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_bid = Bid(
        product_id=bid.product_id,
        buyer_id=current_user.id,
        quantity=bid.quantity,
        price_per_kg=bid.price_per_kg
    )
    db.add(new_bid)

    # ✅ Create Notification for Farmer
    notification = Notification(
        user_id=product.farmer_id,
        message=f"New bid placed on {product.name} by {current_user.full_name}."
    )
    db.add(notification)

    db.commit()
    db.refresh(new_bid)
    return new_bid

# ✅ Farmer views bids on their products
@router.get("/", response_model=list[BidResponse])
def get_bids(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("farmer"))
):
    bids = db.query(Bid).join(Product).filter(Product.farmer_id == current_user.id).all()
    return bids

# ✅ Farmer accepts/rejects a bid
@router.put("/{bid_id}/update", response_model=BidResponse)
def update_bid_status(
    bid_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("farmer"))
):
    bid = db.query(Bid).filter(Bid.id == bid_id).join(Product).filter(Product.farmer_id == current_user.id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")

    if status not in ["accepted", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    bid.status = status

    # ✅ Create Notification for Buyer
    notification = Notification(
        user_id=bid.buyer_id,
        message=f"Your bid on {bid.product.name} was {status} by {current_user.full_name}."
    )
    db.add(notification)

    db.commit()
    db.refresh(bid)
    return bid
