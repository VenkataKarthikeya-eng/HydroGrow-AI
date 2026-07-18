import hashlib
import secrets
import datetime
from sqlalchemy.orm import Session
from backend.database.models import IoTDeviceCredential

class DeviceManager:
    """
    IoT Hardware Device Registry & Authentication Manager.
    Handles device registration, API key hashing, heartbeat state, and security access.
    """

    @staticmethod
    def hash_api_key(api_key: str) -> str:
        return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

    @classmethod
    def register_device(
        cls, 
        db: Session, 
        user_id: int, 
        device_id: str, 
        device_type: str = "ESP32", 
        location: str = "Zone 1 - Main Channel"
    ) -> dict:
        raw_key = f"hg_key_{secrets.token_hex(16)}"
        key_hash = cls.hash_api_key(raw_key)

        existing = db.query(IoTDeviceCredential).filter(IoTDeviceCredential.device_id == device_id).first()
        if existing:
            existing.api_key_hash = key_hash
            existing.device_type = device_type
            existing.location = location
            existing.status = "Active"
            existing.last_seen = datetime.datetime.utcnow()
            db.commit()
            db.refresh(existing)
            device_obj = existing
        else:
            device_obj = IoTDeviceCredential(
                device_id=device_id,
                user_id=user_id,
                api_key_hash=key_hash,
                device_type=device_type,
                location=location,
                status="Active"
            )
            db.add(device_obj)
            db.commit()
            db.refresh(device_obj)

        return {
            "device_id": device_obj.device_id,
            "device_type": device_obj.device_type,
            "location": device_obj.location,
            "api_key": raw_key, # Raw key shown ONLY ONCE on creation
            "status": device_obj.status
        }

    @classmethod
    def authenticate_device(cls, db: Session, device_id: str, api_key: str) -> bool:
        device = db.query(IoTDeviceCredential).filter(IoTDeviceCredential.device_id == device_id).first()
        if not device or device.status != "Active":
            return False
        return device.api_key_hash == cls.hash_api_key(api_key)

    @classmethod
    def update_heartbeat(cls, db: Session, device_id: str) -> bool:
        device = db.query(IoTDeviceCredential).filter(IoTDeviceCredential.device_id == device_id).first()
        if device:
            device.last_seen = datetime.datetime.utcnow()
            device.status = "Active"
            db.commit()
            return True
        return False
