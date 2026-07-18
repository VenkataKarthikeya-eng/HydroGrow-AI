from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import ExpertProfile, ExpertRecommendation
from backend.services.agriculture_intelligence.expert_matching import ExpertMatching
from backend.services.agriculture_intelligence.recommendation_engine import GlobalRecommendationEngine

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

@router.get("/experts", summary="List verified agricultural experts")
def list_experts(db: Session = Depends(get_db)):
    return ExpertMatching.match_experts(db)

@router.post("/experts/request", summary="Request consultation with an agronomist")
def request_consultation(
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    expert_id = payload.get("expert_id")
    issue_description = payload.get("issue_description")
    if not expert_id or not issue_description:
        raise HTTPException(status_code=400, detail="expert_id and issue_description are required.")

    rec = ExpertRecommendation(
        user_id=user.id,
        crop_type=payload.get("crop_type", "Lettuce"),
        recommendation=f"Consultation requested for issue: {issue_description}",
        source="Expert Network",
        confidence_score=98.0
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)

    return {
        "message": "Consultation request dispatched to expert.",
        "request_id": rec.id,
        "status": "Pending Expert Response"
    }

@router.get("/experts/recommendations", summary="Get expert & AI agronomic recommendations")
def get_recommendations(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    recs = GlobalRecommendationEngine.generate_recommendations()
    return recs
