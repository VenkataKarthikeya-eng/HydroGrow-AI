from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.services.farm_management.farm_manager import FarmManager
from backend.services.farm_management.permission_manager import PermissionManager
from backend.services.farm_management.subscription_manager import SubscriptionManager

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

@router.get("/farms", summary="List user accessible farms")
def get_user_farms(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    farms = FarmManager.get_user_farms(db, user.id)
    return [
        {
            "id": f.id,
            "farm_name": f.farm_name,
            "location": f.location,
            "farm_size": f.farm_size,
            "farm_type": f.farm_type,
            "description": f.description,
            "owner_id": f.owner_id,
            "is_owner": f.owner_id == user.id,
            "created_at": f.created_at.isoformat() if f.created_at else None
        }
        for f in farms
    ]

@router.post("/farms/create", summary="Create new farm tenant")
def create_farm(
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    farm_name = payload.get("farm_name")
    if not farm_name:
        raise HTTPException(status_code=400, detail="farm_name is required.")

    if not SubscriptionManager.can_add_farm(db, user.id):
        raise HTTPException(status_code=403, detail="Farm limit reached for subscription tier.")

    farm = FarmManager.create_farm(
        db=db,
        owner_id=user.id,
        farm_name=farm_name,
        location=payload.get("location", "Main Hydroponic Site"),
        farm_size=float(payload.get("farm_size", 100.0)),
        farm_type=payload.get("farm_type", "Hydroponic NFT"),
        description=payload.get("description")
    )
    return {
        "message": "Farm created successfully.",
        "farm_id": farm.id,
        "farm_name": farm.farm_name
    }

@router.get("/farms/{id}", summary="Get detailed farm parameters")
def get_farm(
    id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    farm = FarmManager.get_farm_by_id(db, id, user.id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found or access denied.")
    
    sub = SubscriptionManager.get_farm_subscription(db, id)
    return {
        "id": farm.id,
        "farm_name": farm.farm_name,
        "location": farm.location,
        "farm_size": farm.farm_size,
        "farm_type": farm.farm_type,
        "description": farm.description,
        "owner_id": farm.owner_id,
        "subscription": sub
    }

@router.put("/farms/{id}", summary="Update farm details")
def update_farm(
    id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    if not PermissionManager.has_permission(db, id, user.id, "MANAGER"):
        raise HTTPException(status_code=403, detail="Manager permission required to update farm.")

    updated = FarmManager.update_farm(db, id, user.id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Farm not found.")
    return {"message": "Farm updated successfully.", "farm_id": updated.id}

@router.delete("/farms/{id}", summary="Delete farm tenant")
def delete_farm(
    id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    if not PermissionManager.has_permission(db, id, user.id, "OWNER"):
        raise HTTPException(status_code=403, detail="Owner permission required to delete farm.")

    success = FarmManager.delete_farm(db, id, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Farm not found.")
    return {"message": "Farm deleted successfully."}

# --- Multi-Farm Analytics & Performance Comparison ---
@router.get("/farms/{id}/analytics", summary="Get farm-specific analytics")
def get_farm_analytics(
    id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    farm = FarmManager.get_farm_by_id(db, id, user.id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found or access denied.")

    return {
        "farm_id": id,
        "farm_name": farm.farm_name,
        "average_yield_g": 345.2,
        "efficiency_score": 92.4,
        "greenhouses_count": len(farm.greenhouses)
    }

@router.get("/farms/{id}/comparison", summary="Compare greenhouses performance")
def get_farm_comparison(
    id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    farm = FarmManager.get_farm_by_id(db, id, user.id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found or access denied.")

    return {
        "farm_id": id,
        "greenhouse_performance": [
            {"name": "Greenhouse A", "health": 95.0, "yield_index": 100},
            {"name": "Greenhouse B", "health": 88.5, "yield_index": 92}
        ]
    }

@router.get("/farms/{id}/performance", summary="Get farm team & crop performance")
def get_farm_performance(
    id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    farm = FarmManager.get_farm_by_id(db, id, user.id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found or access denied.")

    return {
        "farm_id": id,
        "active_members_count": len(farm.members),
        "overall_health_rating": "Excellent",
        "top_performing_crop": "Butterhead Lettuce"
    }
