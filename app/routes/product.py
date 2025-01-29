from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.db.database import engine
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse
from app.utils.auth import get_current_user, require_role

router = APIRouter()

# ✅ Dependency to get the database session
def get_db():
    with Session(engine) as session:
        yield session

# ✅ Farmer can add a new product
@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("farmer"))
):
    new_product = Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        image_url=product.image_url,
        farmer_id=current_user.id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# ✅ Get all available products (Include Farmer Name & Phone)
@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    # ✅ Fetch all products and join with farmers
    products = db.query(Product).options(joinedload(Product.farmer)).all()

    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            quantity=product.quantity,
            image_url=product.image_url,
            farmer={
                "id": product.farmer.id,
                "full_name": product.farmer.full_name,
                "phone": product.farmer.phone
            }
        )
        for product in products
    ]
