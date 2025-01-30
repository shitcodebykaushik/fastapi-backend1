from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import get_db
from app.models.insurance import Insurance, UserInsurance
from app.models.user import User
from app.schemas.insurance import InsuranceResponse
from app.utils.auth import get_current_user

router = APIRouter()

# ✅ 1️⃣ Get Available Insurance Plans (Filtered by User Role)
@router.get("/", response_model=list[InsuranceResponse])
def get_insurance_plans(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    plans = db.query(Insurance).filter(Insurance.user_type == current_user.role).all()

    if not plans:
        raise HTTPException(
            status_code=404, detail="No insurance plans available for your role."
        )

    return plans


# ✅ 2️⃣ Apply for Insurance
@router.post("/apply")
def apply_for_insurance(
    insurance_id: int = Query(..., description="ID of the insurance plan"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if insurance exists
    insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance plan not found.")

    # Ensure the user is eligible
    if insurance.user_type != current_user.role:
        raise HTTPException(
            status_code=403, detail="You are not eligible for this insurance plan."
        )

    # Check if user has already applied
    existing_policy = (
        db.query(UserInsurance)
        .filter(
            UserInsurance.user_id == current_user.id,
            UserInsurance.insurance_id == insurance_id,
        )
        .first()
    )
    if existing_policy:
        raise HTTPException(
            status_code=400, detail="You have already applied for this insurance."
        )

    # Apply for insurance
    user_insurance = UserInsurance(user_id=current_user.id, insurance_id=insurance_id)
    db.add(user_insurance)
    db.commit()
    db.refresh(user_insurance)

    return {"message": "Insurance applied successfully!", "insurance_id": user_insurance.id}


# ✅ 3️⃣ Claim Insurance
@router.post("/claim")
def claim_insurance(
    insurance_id: int = Query(..., description="ID of the insurance plan"),
    reason: str = Query(..., description="Reason for claiming the insurance"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if user has applied for this insurance
    user_insurance = (
        db.query(UserInsurance)
        .filter(
            UserInsurance.user_id == current_user.id,
            UserInsurance.insurance_id == insurance_id,
            UserInsurance.status == "active",
        )
        .first()
    )

    if not user_insurance:
        raise HTTPException(
            status_code=404, detail="You do not have an active policy for this insurance."
        )

    # Ensure insurance is not already claimed
    if user_insurance.status == "claimed":
        raise HTTPException(
            status_code=400, detail="You have already claimed this insurance."
        )

    # Claim the insurance
    user_insurance.status = "claimed"
    user_insurance.claimed_at = datetime.utcnow()
    db.commit()

    return {
        "message": "Insurance claim submitted successfully!",
        "insurance_id": user_insurance.id,
    }
