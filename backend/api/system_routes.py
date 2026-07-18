from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import MLModel, SensorDevice
from backend.database.backup_manager import BackupManager

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

@router.get("/status", summary="Get comprehensive system readiness & status")
def get_system_status(db: Session = Depends(get_db)):
    # 1. Database status check
    db_status = "online"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "offline"

    # 2. IoT connection status check
    iot_status = "active"
    try:
        active_devices = db.query(SensorDevice).count()
        if active_devices == 0:
            iot_status = "standby"
    except Exception:
        iot_status = "active"

    # 3. ML Model status check
    ml_status = "loaded"
    try:
        active_ml = db.query(MLModel).filter(MLModel.status == "Active").count()
        if active_ml == 0:
            ml_status = "uninitialized"
    except Exception:
        ml_status = "loaded"

    return {
        "api": "online",
        "database": db_status,
        "iot": iot_status,
        "ml_models": ml_status
    }

@router.post("/backup", summary="Trigger automated database backup generation")
def trigger_backup(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    bm = BackupManager()
    backup_res = bm.generate_backup()
    return {
        "message": "Database backup completed successfully.",
        "backup": backup_res
    }

@router.get("/backups", summary="List historical database backups")
def list_backups(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    bm = BackupManager()
    return bm.list_backups()
