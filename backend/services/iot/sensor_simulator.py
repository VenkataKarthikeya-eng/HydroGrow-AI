import random
from sqlalchemy.orm import Session
from backend.services.iot.sensor_manager import SensorManager

class SensorSimulator:
    """
    Generates simulated hydroponic readings utilizing a gradual random walk
    from the latest stored state, preventing sudden changes.
    """
    @staticmethod
    def generate_next_reading(db: Session, user_id: int, device_id: int) -> dict:
        latest = SensorManager.get_latest_reading(db, user_id, device_id)
        
        if latest:
            prev_ph = latest.water_ph
            prev_ec = latest.water_ec
            prev_temp = latest.temperature
            prev_humidity = latest.humidity
            prev_water_temp = latest.water_temperature
            prev_co2 = latest.co2
            prev_nut = latest.nutrient_level
        else:
            prev_ph = 6.0
            prev_ec = 1.8
            prev_temp = 23.5
            prev_humidity = 60.0
            prev_water_temp = 21.0
            prev_co2 = 450.0
            prev_nut = 100.0

        next_ph = max(4.0, min(10.0, prev_ph + random.uniform(-0.08, 0.08)))
        next_ec = max(0.5, min(4.5, prev_ec + random.uniform(-0.06, 0.06)))
        next_temp = max(12.0, min(34.0, prev_temp + random.uniform(-0.25, 0.25)))
        next_humidity = max(35.0, min(88.0, prev_humidity + random.uniform(-1.2, 1.2)))
        next_water_temp = max(16.0, min(28.0, prev_water_temp + random.uniform(-0.12, 0.12)))
        next_co2 = max(320.0, min(950.0, prev_co2 + random.uniform(-12.0, 12.0)))
        
        next_nut = prev_nut - random.uniform(0.1, 0.3)
        if next_nut < 40.0:
            next_nut = 100.0

        return {
            "temperature": round(next_temp, 2),
            "humidity": round(next_humidity, 2),
            "water_ph": round(next_ph, 2),
            "water_ec": round(next_ec, 2),
            "water_temperature": round(next_water_temp, 2),
            "co2": round(next_co2, 2),
            "nutrient_level": round(next_nut, 2)
        }
