from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import CropTemplateLibrary

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

@router.get("/templates", summary="List crop growing templates in global library")
def list_templates(db: Session = Depends(get_db)):
    templates = db.query(CropTemplateLibrary).all()

    if not templates:
        # Seed default templates
        t1 = CropTemplateLibrary(
            creator_id=1,
            crop_name="Butterhead Lettuce NFT High Yield",
            variety="Rex Butterhead",
            nutrient_profile={"nitrogen": 160, "phosphorus": 50, "potassium": 210, "calcium": 180},
            environmental_profile={"temp_day": 22.0, "temp_night": 18.0, "ph": 6.0, "ec": 1.9},
            growth_duration=35,
            success_rate=98.2,
            downloads=42
        )
        t2 = CropTemplateLibrary(
            creator_id=1,
            crop_name="Romaine Hydroponic Aeroponic Speed Grow",
            variety="Parris Island",
            nutrient_profile={"nitrogen": 170, "phosphorus": 55, "potassium": 220, "calcium": 190},
            environmental_profile={"temp_day": 21.5, "temp_night": 17.5, "ph": 6.1, "ec": 2.0},
            growth_duration=30,
            success_rate=96.5,
            downloads=28
        )
        db.add(t1)
        db.add(t2)
        db.commit()
        templates = [t1, t2]

    return [
        {
            "id": t.id,
            "crop_name": t.crop_name,
            "variety": t.variety,
            "nutrient_profile": t.nutrient_profile,
            "environmental_profile": t.environmental_profile,
            "growth_duration": t.growth_duration,
            "success_rate": t.success_rate,
            "downloads": t.downloads,
            "creator_id": t.creator_id,
            "created_at": t.created_at.isoformat() if t.created_at else None
        }
        for t in templates
    ]

@router.post("/templates/create", summary="Publish crop growing template")
def create_template(
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    crop_name = payload.get("crop_name")
    if not crop_name:
        raise HTTPException(status_code=400, detail="crop_name is required.")

    template = CropTemplateLibrary(
        creator_id=user.id,
        crop_name=crop_name,
        variety=payload.get("variety", "Standard"),
        nutrient_profile=payload.get("nutrient_profile", {"nitrogen": 150, "potassium": 200}),
        environmental_profile=payload.get("environmental_profile", {"temp_day": 22.0, "ph": 6.0, "ec": 1.8}),
        growth_duration=int(payload.get("growth_duration", 35)),
        success_rate=float(payload.get("success_rate", 95.0))
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    return {"message": "Crop template published successfully.", "template_id": template.id}

@router.post("/templates/download/{id}", summary="Download & apply crop template to farm")
def download_template(
    id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    template = db.query(CropTemplateLibrary).filter(CropTemplateLibrary.id == id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found.")

    template.downloads += 1
    db.commit()
    return {
        "message": f"Template '{template.crop_name}' applied to active farm environment.",
        "template": {
            "id": template.id,
            "crop_name": template.crop_name,
            "variety": template.variety,
            "nutrient_profile": template.nutrient_profile,
            "environmental_profile": template.environmental_profile
        }
    }
