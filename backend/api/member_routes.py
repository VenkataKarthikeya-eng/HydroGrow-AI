from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import FarmMember, User
from backend.services.farm_management.permission_manager import PermissionManager

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

@router.get("/farms/{farm_id}/members", summary="List team members of a farm")
def list_farm_members(
    farm_id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    if not PermissionManager.has_permission(db, farm_id, user.id, "VIEWER"):
        raise HTTPException(status_code=403, detail="Access denied to this farm.")

    members = db.query(FarmMember).filter(FarmMember.farm_id == farm_id).all()
    return [
        {
            "id": m.id,
            "user_id": m.user_id,
            "username": m.user.username if m.user else "User",
            "email": m.user.email if m.user else "",
            "role": m.role,
            "joined_at": m.joined_at.isoformat()
        }
        for m in members
    ]

@router.post("/farms/{farm_id}/members/add", summary="Invite/Add team member to farm")
def add_farm_member(
    farm_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    if not PermissionManager.has_permission(db, farm_id, user.id, "OWNER"):
        raise HTTPException(status_code=403, detail="Owner permission required to add members.")

    email = payload.get("email")
    role = payload.get("role", "WORKER").upper()

    target_user = db.query(User).filter(User.email == email).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User with this email not found.")

    existing = db.query(FarmMember).filter(
        FarmMember.farm_id == farm_id,
        FarmMember.user_id == target_user.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User is already a member of this farm.")

    member = FarmMember(
        farm_id=farm_id,
        user_id=target_user.id,
        role=role
    )
    db.add(member)
    db.commit()
    db.refresh(member)

    return {"message": f"User {email} added as {role}.", "member_id": member.id}

@router.put("/farms/{farm_id}/members/{id}/role", summary="Update team member role")
def update_member_role(
    farm_id: int,
    id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    if not PermissionManager.has_permission(db, farm_id, user.id, "OWNER"):
        raise HTTPException(status_code=403, detail="Owner permission required to update roles.")

    new_role = payload.get("role", "WORKER").upper()
    member = db.query(FarmMember).filter(
        FarmMember.id == id,
        FarmMember.farm_id == farm_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member record not found.")

    member.role = new_role
    db.commit()
    return {"message": "Member role updated successfully.", "role": new_role}

@router.delete("/farms/{farm_id}/members/{id}", summary="Remove member from farm")
def remove_farm_member(
    farm_id: int,
    id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    if not PermissionManager.has_permission(db, farm_id, user.id, "OWNER"):
        raise HTTPException(status_code=403, detail="Owner permission required to remove members.")

    member = db.query(FarmMember).filter(
        FarmMember.id == id,
        FarmMember.farm_id == farm_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member record not found.")

    db.delete(member)
    db.commit()
    return {"message": "Member removed from farm."}
