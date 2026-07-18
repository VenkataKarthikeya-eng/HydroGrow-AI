from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Any
from pydantic import BaseModel, Field
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.services.iot.sensor_manager import SensorManager
from backend.services.iot.sensor_simulator import SensorSimulator
from backend.services.iot.data_processor import DataProcessor
from backend.services.iot.alert_engine import AlertEngine
from backend.api.websocket_routes import ws_manager
from backend.services.automation.automation_engine import AutomationEngine

router = APIRouter()

class DeviceRegister(BaseModel):
    device_name: str = Field(..., min_length=2, max_length=50)
    location: str = Field(default="Grow Room 1")
    device_type: str = Field(default="Hydroponic Tank Sensor")

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing, invalid, or expired."
        )
    return current_user

@router.get("/devices", summary="Get user's registered IoT devices")
def get_devices(db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    devices = SensorManager.get_user_devices(db, user.id)
    return [
        {
            "id": d.id, 
            "device_name": d.device_name, 
            "location": d.location, 
            "device_type": d.device_type, 
            "status": d.status
        } 
        for d in devices
    ]

@router.post("/devices", summary="Register a new sensor device")
def register_device(data: DeviceRegister, db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    device = SensorManager.register_sensor(db, user.id, data.device_name, data.location, data.device_type)
    return {
        "id": device.id, 
        "device_name": device.device_name, 
        "location": device.location, 
        "device_type": device.device_type
    }

@router.get("/latest", summary="Get the latest reading for a device")
def get_latest(device_id: int, db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    device = SensorManager.get_sensor_device(db, user.id, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found or access denied.")
    reading = SensorManager.get_latest_reading(db, user.id, device_id)
    if not reading:
        return {}
    return {
        "temperature": reading.temperature,
        "humidity": reading.humidity,
        "water_ph": reading.water_ph,
        "water_ec": reading.water_ec,
        "water_temperature": reading.water_temperature,
        "co2": reading.co2,
        "nutrient_level": reading.nutrient_level,
        "timestamp": reading.timestamp.isoformat() if reading.timestamp else None
    }

@router.get("/history", summary="Get sensor reading historical timeline")
def get_history(device_id: int, limit: int = 100, db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    device = SensorManager.get_sensor_device(db, user.id, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found or access denied.")
    readings = SensorManager.get_readings_history(db, user.id, device_id, limit=limit)
    return [
        {
            "temperature": r.temperature,
            "humidity": r.humidity,
            "water_ph": r.water_ph,
            "water_ec": r.water_ec,
            "water_temperature": r.water_temperature,
            "co2": r.co2,
            "nutrient_level": r.nutrient_level,
            "timestamp": r.timestamp.isoformat() if r.timestamp else None
        }
        for r in reversed(readings)
    ]

@router.get("/alerts", summary="Get active unresolved alerts")
def get_alerts(db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    from backend.database.models import Alert
    alerts = db.query(Alert).filter(Alert.user_id == user.id, Alert.resolved == False).all()
    return [
        {
            "id": a.id,
            "alert_type": a.alert_type,
            "severity": a.severity,
            "parameter": a.parameter,
            "message": a.message,
            "created_at": a.created_at.isoformat() if a.created_at else None
        }
        for a in alerts
    ]

@router.post("/simulate", summary="Trigger a simulated sensor reading tick")
async def simulate_reading(device_id: int, db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    device = SensorManager.get_sensor_device(db, user.id, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found or access denied.")
    
    sim_data = SensorSimulator.generate_next_reading(db, user.id, device_id)
    
    # Range validations check
    if not DataProcessor.validate_reading(sim_data):
        raise HTTPException(status_code=400, detail="Invalid simulated sensor values generated.")
        
    averages = DataProcessor.calculate_moving_averages(db, user.id, device_id, sim_data)
    
    reading = SensorManager.save_sensor_reading(
        db, 
        device_id,
        sim_data["temperature"],
        sim_data["humidity"],
        sim_data["water_ph"],
        sim_data["water_ec"],
        sim_data["water_temperature"],
        sim_data["co2"],
        sim_data["nutrient_level"]
    )
    
    alerts = AlertEngine.analyze_readings_for_alerts(db, user.id, sim_data, averages)
    
    automation_events = AutomationEngine.process_sensor_update(db, user.id, reading.id, sim_data)
    
    payload = {
        "device_id": device_id,
        "reading": {
            "temperature": reading.temperature,
            "humidity": reading.humidity,
            "water_ph": reading.water_ph,
            "water_ec": reading.water_ec,
            "water_temperature": reading.water_temperature,
            "co2": reading.co2,
            "nutrient_level": reading.nutrient_level,
            "timestamp": reading.timestamp.isoformat()
        },
        "averages": averages,
        "alerts": alerts,
        "automation_events": automation_events
    }
    
    # Push to live socket channels
    await ws_manager.broadcast_to_user(user.id, payload)
    
    return payload
