from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.services.farm_management.greenhouse_manager import GreenhouseManager
from backend.services.farm_management.permission_manager import PermissionManager

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

@router.get("/greenhouses", summary="List greenhouses for a farm")
def list_greenhouses(
    farm_id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    if not PermissionManager.has_permission(db, farm_id, user.id, "VIEWER"):
        raise HTTPException(status_code=403, detail="Access denied to this farm.")

    greenhouses = GreenhouseManager.list_greenhouses(db, farm_id)
    return [
        {
            "id": g.id,
            "farm_id": g.farm_id,
            "name": g.name,
            "area_size": g.area_size,
            "environment_type": g.environment_type,
            "automation_enabled": g.automation_enabled
        }
        for g in greenhouses
    ]

@router.post("/greenhouses/create", summary="Create new greenhouse growing zone")
def create_greenhouse(
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    farm_id = payload.get("farm_id")
    name = payload.get("name")
    if not farm_id or not name:
        raise HTTPException(status_code=400, detail="farm_id and name are required.")

    if not PermissionManager.has_permission(db, farm_id, user.id, "MANAGER"):
        raise HTTPException(status_code=403, detail="Manager permission required to create greenhouse.")

    gh = GreenhouseManager.create_greenhouse(
        db=db,
        farm_id=farm_id,
        name=name,
        area_size=float(payload.get("area_size", 50.0)),
        environment_type=payload.get("environment_type", "NFT Hydroponics")
    )
    return {"message": "Greenhouse created successfully.", "greenhouse_id": gh.id}

@router.get("/greenhouses/{id}", summary="Get greenhouse details & status")
def get_greenhouse(
    id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    status_data = GreenhouseManager.get_greenhouse_status(db, id)
    if not status_data:
        raise HTTPException(status_code=404, detail="Greenhouse not found.")
    return status_data
