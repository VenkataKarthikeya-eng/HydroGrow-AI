import datetime
from sqlalchemy.orm import Session
from backend.database.models import DeviceTelemetryLog

class TelemetryProcessor:
    """
    Hardware Sensor Telemetry Ingestion Pipeline.
    Processes, validates, filters noise, normalizes, and logs hardware readings.
    """

    @staticmethod
    def process_telemetry(db: Session, raw_payload: dict) -> dict:
        device_id = raw_payload.get("device_id", "ESP32_001")
        
        # 1. Bounds checking & noise filtering
        temp = max(10.0, min(45.0, float(raw_payload.get("temperature", raw_payload.get("air_temperature", 24.5)))))
        humidity = max(20.0, min(100.0, float(raw_payload.get("humidity", 65.0))))
        water_ph = max(3.0, min(10.0, float(raw_payload.get("water_ph", raw_payload.get("ph", 6.2)))))
        water_ec = max(0.2, min(5.0, float(raw_payload.get("water_ec", raw_payload.get("ec", 2.0)))))
        water_temp = max(10.0, min(40.0, float(raw_payload.get("water_temperature", 22.0))))
        co2 = max(300.0, min(2000.0, float(raw_payload.get("co2", 450.0))))
        nutrient_level = max(0.0, min(100.0, float(raw_payload.get("nutrient_level", 85.0))))

        clean_sensor_data = {
            "temperature": round(temp, 2),
            "humidity": round(humidity, 2),
            "water_ph": round(water_ph, 2),
            "water_ec": round(water_ec, 2),
            "water_temperature": round(water_temp, 2),
            "co2": round(co2, 2),
            "nutrient_level": round(nutrient_level, 2)
        }

        # 2. Persist in database
        log_entry = DeviceTelemetryLog(
            device_id=device_id,
            sensor_data=clean_sensor_data,
            processing_status="Processed"
        )
        db.add(log_entry)
        db.commit()

        # 3. Format structured broadcast payload
        return {
            "type": "sensor_update",
            "device": device_id,
            "data": clean_sensor_data,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
