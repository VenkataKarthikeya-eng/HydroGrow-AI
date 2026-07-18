from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional, Dict, Any
from backend.database.models import SensorDevice, SensorReading, Alert

class SensorManager:
    """
    Manages IoT sensor devices registration, ping statuses, readings commits,
    and historic log queries bounded by user isolation constraints.
    """
    @staticmethod
    def register_sensor(
        db: Session, 
        user_id: int, 
        device_name: str, 
        location: str = "Grow Room 1", 
        device_type: str = "Hydroponic Tank Sensor"
    ) -> SensorDevice:
        device = SensorDevice(
            user_id=user_id,
            device_name=device_name,
            location=location,
            device_type=device_type,
            status="active"
        )
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def get_user_devices(db: Session, user_id: int) -> List[SensorDevice]:
        return db.query(SensorDevice).filter(SensorDevice.user_id == user_id).all()

    @staticmethod
    def get_sensor_device(db: Session, user_id: int, device_id: int) -> Optional[SensorDevice]:
        return db.query(SensorDevice).filter(
            SensorDevice.id == device_id, 
            SensorDevice.user_id == user_id
        ).first()

    @staticmethod
    def save_sensor_reading(
        db: Session, 
        device_id: int, 
        temperature: float, 
        humidity: float, 
        water_ph: float, 
        water_ec: float, 
        water_temperature: float, 
        co2: float, 
        nutrient_level: float = 100.0
    ) -> SensorReading:
        reading = SensorReading(
            device_id=device_id,
            temperature=temperature,
            humidity=humidity,
            water_ph=water_ph,
            water_ec=water_ec,
            water_temperature=water_temperature,
            co2=co2,
            nutrient_level=nutrient_level,
            timestamp=datetime.utcnow()
        )
        db.add(reading)
        db.commit()
        db.refresh(reading)
        return reading

    @staticmethod
    def get_latest_reading(db: Session, user_id: int, device_id: int) -> Optional[SensorReading]:
        # Join with SensorDevice to ensure user isolation
        return (
            db.query(SensorReading)
            .join(SensorDevice)
            .filter(
                SensorReading.device_id == device_id,
                SensorDevice.user_id == user_id
            )
            .order_by(SensorReading.timestamp.desc())
            .first()
        )

    @staticmethod
    def get_readings_history(
        db: Session, 
        user_id: int, 
        device_id: int, 
        limit: int = 100
    ) -> List[SensorReading]:
        return (
            db.query(SensorReading)
            .join(SensorDevice)
            .filter(
                SensorReading.device_id == device_id,
                SensorDevice.user_id == user_id
            )
            .order_by(SensorReading.timestamp.desc())
            .limit(limit)
            .all()
        )
