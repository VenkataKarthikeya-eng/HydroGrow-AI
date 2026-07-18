from sqlalchemy.orm import Session
from backend.database.models import DigitalTwinProfile, SimulationRun, SimulationParameters, GrowthForecast, Prediction, SensorReading, SensorDevice, PlantAnalysis, PlantImage

class TwinEngine:
    """
    Orchestrates Digital Twin virtual profile configuration,
    scenario comparison simulations, and historical prediction aggregation.
    """
    @staticmethod
    def resolve_farm_baseline_conditions(db: Session, user_id: int) -> dict:
        conditions = {
            "temperature": 22.0,
            "humidity": 60.0,
            "co2": 450.0,
            "water_ph": 6.2,
            "water_ec": 2.0,
            "light_hours": 16.0
        }

        # 1. IoT telemetry
        latest_reading = (
            db.query(SensorReading)
            .join(SensorDevice)
            .filter(SensorDevice.user_id == user_id)
            .order_by(SensorReading.timestamp.desc())
            .first()
        )
        if latest_reading:
            conditions["temperature"] = latest_reading.temperature
            conditions["humidity"] = latest_reading.humidity
            conditions["co2"] = latest_reading.co2
            conditions["water_ph"] = latest_reading.water_ph
            conditions["water_ec"] = latest_reading.water_ec

        # 2. Predictions parameters
        latest_pred = (
            db.query(Prediction)
            .filter(Prediction.user_id == user_id)
            .order_by(Prediction.created_at.desc())
            .first()
        )
        if latest_pred and isinstance(latest_pred.input_parameters, dict):
            params = latest_pred.input_parameters
            if "light_hours" in params:
                conditions["light_hours"] = params["light_hours"]

        return conditions

    @staticmethod
    def create_virtual_profile(
        db: Session, 
        user_id: int, 
        farm_name: str, 
        system_type: str, 
        area_size: float, 
        lighting_setup: str, 
        nutrient_system: str
    ) -> DigitalTwinProfile:
        # Check if profile already exists, update it or create new
        profile = db.query(DigitalTwinProfile).filter(DigitalTwinProfile.user_id == user_id).first()
        if not profile:
            profile = DigitalTwinProfile(
                user_id=user_id,
                farm_name=farm_name,
                crop_type="Lettuce",
                system_type=system_type,
                area_size=area_size,
                lighting_setup=lighting_setup,
                nutrient_system=nutrient_system
            )
            db.add(profile)
        else:
            profile.farm_name = farm_name
            profile.system_type = system_type
            profile.area_size = area_size
            profile.lighting_setup = lighting_setup
            profile.nutrient_system = nutrient_system
            
        db.commit()
        db.refresh(profile)
        return profile
