from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.user import User, Base
from app.schemas.user import UserCreate, UserResponse
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter()
Base.metadata.create_all(bind=engine)  # Ensure the table is created

# Dependency to get the database session
def get_db():
    with Session(engine) as session:
        yield session

# User Signup API
@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.email == user.email) | (User.phone == user.phone)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# User Login API
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))

    return {"access_token": access_token, "token_type": "bearer"}

# Get the current logged-in user (Protected route)
@router.get("/me", response_model=UserResponse)
def get_logged_in_user(current_user=Depends(get_current_user)):
    return current_user
