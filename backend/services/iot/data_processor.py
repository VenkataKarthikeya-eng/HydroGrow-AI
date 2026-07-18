from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.services.iot.sensor_manager import SensorManager

class DataProcessor:
    """
    Validates sensor reading parameter bounds and calculates moving averages
    to facilitate smooth environmental trend calculations.
    """
    @staticmethod
    def validate_reading(data: dict) -> bool:
        temp = data.get("temperature")
        hum = data.get("humidity")
        ph = data.get("water_ph")
        ec = data.get("water_ec")
        co2 = data.get("co2")

        if temp is None or not (0.0 <= float(temp) <= 50.0):
            return False
        if hum is None or not (0.0 <= float(hum) <= 100.0):
            return False
        if ph is None or not (0.0 <= float(ph) <= 14.0):
            return False
        if ec is None or not (0.0 <= float(ec) <= 10.0):
            return False
        if co2 is None or not (0.0 <= float(co2) <= 5000.0):
            return False
        return True

    @staticmethod
    def calculate_moving_averages(db: Session, user_id: int, device_id: int, current_reading: dict) -> dict:
        history = SensorManager.get_readings_history(db, user_id, device_id, limit=4)
        readings = [current_reading] + [
            {
                "temperature": h.temperature,
                "humidity": h.humidity,
                "water_ph": h.water_ph,
                "water_ec": h.water_ec,
                "water_temperature": h.water_temperature,
                "co2": h.co2,
                "nutrient_level": h.nutrient_level
            }
            for h in history
        ]
        
        avg = {}
        for key in ["temperature", "humidity", "water_ph", "water_ec", "water_temperature", "co2", "nutrient_level"]:
            vals = [float(r.get(key, 0.0)) for r in readings if key in r]
            avg[key] = round(sum(vals) / len(vals), 2) if vals else 0.0
        return avg
