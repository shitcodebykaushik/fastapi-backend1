from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notificaton import NotificationResponse
from app.utils.auth import get_current_user

router = APIRouter()

# ✅ Dependency to get the database session
def get_db():
    with Session(engine) as session:
        yield session

# ✅ Get notifications for the logged-in user
@router.get("/", response_model=list[NotificationResponse])
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Notification).filter(Notification.user_id == current_user.id).all()
