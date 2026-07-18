from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import IoTDeviceCredential, DeviceTelemetryLog, CloudDeploymentLog
from backend.cloud.device_manager import DeviceManager
from backend.cloud.telemetry_processor import TelemetryProcessor
from backend.cloud.cloud_storage import CloudStorageProvider
from backend.cloud.mqtt_service import MQTTService
from backend.mlops.model_registry import ModelRegistry
from backend.mlops.training_scheduler import TrainingScheduler
from backend.mlops.model_monitor import ModelMonitor

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

# --- Cloud Infrastructure & Status ---
@router.get("/cloud/status", summary="Get cloud deployment readiness & infrastructure status")
def get_cloud_status(db: Session = Depends(get_db)):
    storage = CloudStorageProvider()
    mqtt = MQTTService()
    mqtt.connect_device("CloudGateway_01")
    
    devices_count = db.query(IoTDeviceCredential).filter(IoTDeviceCredential.status == "Active").count()
    
    return {
        "status": "online",
        "services": {
            "api_backend": "online",
            "database": "online",
            "cloud_storage": f"active ({storage.provider})",
            "mqtt_broker": "connected (local_fallback)" if mqtt.connected else "offline"
        },
        "active_devices_count": devices_count,
        "region": "us-east-1 / AWS Cloud compatible",
        "environment": "production"
    }

# --- IoT Device Management Endpoints ---
@router.get("/devices", summary="List registered hardware IoT devices")
def list_devices(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    devices = db.query(IoTDeviceCredential).filter(IoTDeviceCredential.user_id == user.id).all()
    return [
        {
            "id": d.id,
            "device_id": d.device_id,
            "device_type": d.device_type,
            "location": d.location,
            "status": d.status,
            "last_seen": d.last_seen.isoformat() if d.last_seen else None
        }
        for d in devices
    ]

@router.post("/devices/register", summary="Register new ESP32, Raspberry Pi, or Arduino device")
def register_device(
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    device_id = payload.get("device_id")
    device_type = payload.get("device_type", "ESP32")
    location = payload.get("location", "Zone 1 - Main Channel")

    if not device_id:
        raise HTTPException(status_code=400, detail="device_id is required.")

    res = DeviceManager.register_device(
        db=db,
        user_id=user.id,
        device_id=device_id,
        device_type=device_type,
        location=location
    )
    return res

@router.post("/devices/{id}/connect", summary="Send hardware heartbeat ping")
def connect_device(
    id: str,
    db: Session = Depends(get_db),
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key:
        valid = DeviceManager.authenticate_device(db, id, x_api_key)
        if not valid:
            raise HTTPException(status_code=401, detail="Invalid IoT Device API Key.")

    updated = DeviceManager.update_heartbeat(db, id)
    if not updated:
        raise HTTPException(status_code=44, detail="Device not found.")

    return {"status": "connected", "device_id": id}

@router.get("/devices/{id}/telemetry", summary="Get hardware telemetry history")
def get_device_telemetry(
    id: str,
    db: Session = Depends(get_db)
):
    logs = db.query(DeviceTelemetryLog).filter(
        DeviceTelemetryLog.device_id == id
    ).order_by(DeviceTelemetryLog.received_timestamp.desc()).limit(50).all()

    return [
        {
            "id": l.id,
            "device_id": l.device_id,
            "sensor_data": l.sensor_data,
            "received_timestamp": l.received_timestamp.isoformat()
        }
        for l in logs
    ]

@router.post("/devices/{id}/telemetry", summary="Ingest hardware sensor payload (ESP32/Raspberry Pi/Arduino)")
def ingest_device_telemetry(
    id: str,
    payload: dict,
    db: Session = Depends(get_db)
):
    payload["device_id"] = id
    processed = TelemetryProcessor.process_telemetry(db, payload)
    DeviceManager.update_heartbeat(db, id)
    return processed

# --- MLOps Platform Endpoints ---
@router.get("/mlops/models", summary="List MLOps registered models")
def get_mlops_models(db: Session = Depends(get_db)):
    return ModelRegistry.list_models(db)

@router.post("/mlops/train", summary="Trigger automated MLOps model re-training job")
def trigger_mlops_train(db: Session = Depends(get_db)):
    check = TrainingScheduler.check_retrain_needed(db)
    res = TrainingScheduler.trigger_automated_retraining(db)
    return {
        "check": check,
        "result": res
    }

@router.get("/mlops/monitor", summary="Get real-time model accuracy drift & latency profile")
def get_mlops_monitor(db: Session = Depends(get_db)):
    return ModelMonitor.get_monitoring_metrics(db)
