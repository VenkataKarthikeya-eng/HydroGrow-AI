from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import AutomationRule, AutomationEvent, CropCycle
from backend.services.automation.crop_lifecycle_manager import CropLifecycleManager
from backend.services.automation.optimization_engine import OptimizationEngine

router = APIRouter()
crops_router = APIRouter()

class RuleCreate(BaseModel):
    rule_name: str = Field(..., min_length=2, max_length=50)
    parameter: str = Field(...) # temperature, water_ph, water_ec, humidity, co2
    condition: str = Field(...) # above, below
    threshold_value: float = Field(...)
    action_type: str = Field(default="activate")
    action_value: str = Field(...)
    enabled: bool = Field(default=True)

class CropCreate(BaseModel):
    crop_name: str = Field(..., min_length=2, max_length=50)
    expected_harvest_days: int = Field(default=30)

class CropUpdate(BaseModel):
    current_stage: str = Field(...) # Seedling, Vegetative, Maturity, Harvest

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing, invalid, or expired."
        )
    return current_user

# --- Automation Rules CRUD ---
@router.post("/rules")
def create_rule(data: RuleCreate, db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    rule = AutomationRule(
        user_id=user.id,
        rule_name=data.rule_name,
        parameter=data.parameter,
        condition=data.condition,
        threshold_value=data.threshold_value,
        action_type=data.action_type,
        action_value=data.action_value,
        enabled=data.enabled
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@router.get("/rules")
def get_rules(db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    return db.query(AutomationRule).filter(AutomationRule.user_id == user.id).all()

@router.put("/rules/{id}")
def update_rule(id: int, data: RuleCreate, db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    rule = db.query(AutomationRule).filter(AutomationRule.id == id, AutomationRule.user_id == user.id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found or access denied.")
    rule.rule_name = data.rule_name
    rule.parameter = data.parameter
    rule.condition = data.condition
    rule.threshold_value = data.threshold_value
    rule.action_type = data.action_type
    rule.action_value = data.action_value
    rule.enabled = data.enabled
    db.commit()
    db.refresh(rule)
    return rule

@router.delete("/rules/{id}")
def delete_rule(id: int, db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    rule = db.query(AutomationRule).filter(AutomationRule.id == id, AutomationRule.user_id == user.id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found or access denied.")
    db.delete(rule)
    db.commit()
    return {"message": "Rule deleted successfully."}

# --- Automation Events ---
@router.get("/events")
def get_events(limit: int = 50, db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    events = db.query(AutomationEvent).filter(AutomationEvent.user_id == user.id).order_by(AutomationEvent.created_at.desc()).limit(limit).all()
    return [
        {
            "id": e.id,
            "message": e.message,
            "status": e.status,
            "created_at": e.created_at.isoformat() if e.created_at else None
        }
        for e in events
    ]

# --- Crop Lifecycle Management ---
@crops_router.post("")
def create_crop(data: CropCreate, db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    db.query(CropCycle).filter(CropCycle.user_id == user.id, CropCycle.status == "active").update({"status": "completed"})
    db.commit()
    
    cycle = CropLifecycleManager.create_crop_cycle(db, user.id, data.crop_name, expected_harvest_days=data.expected_harvest_days)
    return cycle

@crops_router.get("/current")
def get_current_crop(db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    cycle = db.query(CropCycle).filter(CropCycle.user_id == user.id, CropCycle.status == "active").first()
    if not cycle:
        return {}
        
    progress = CropLifecycleManager.calculate_growth_progress(cycle.start_date, cycle.expected_harvest_date)
    cycle.growth_progress = progress
    db.commit()
    
    remaining = (cycle.expected_harvest_date - datetime.utcnow()).days
    days_remaining = max(0, remaining)
    
    return {
        "id": cycle.id,
        "crop_name": cycle.crop_name,
        "current_stage": cycle.current_stage,
        "start_date": cycle.start_date.isoformat(),
        "expected_harvest_date": cycle.expected_harvest_date.isoformat(),
        "growth_progress": cycle.growth_progress,
        "days_remaining": days_remaining,
        "status": cycle.status
    }

@crops_router.put("/{id}")
def update_crop(id: int, data: CropUpdate, db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    try:
        cycle = CropLifecycleManager.update_growth_stage(db, user.id, id, data.current_stage)
        return cycle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- AI Optimization Suggestions ---
@router.get("/recommendations")
def get_recommendations(db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    return OptimizationEngine.generate_recommendations(db, user.id)
