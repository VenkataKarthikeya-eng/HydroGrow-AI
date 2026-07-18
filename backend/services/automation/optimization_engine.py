from sqlalchemy.orm import Session
from backend.services.iot.sensor_manager import SensorManager
from backend.database.models import SensorDevice

class OptimizationEngine:
    """
    Analyzes historical data and current sensor values to output
    lettuce optimization suggestions (yield, water, nutrient).
    """
    @staticmethod
    def generate_recommendations(db: Session, user_id: int) -> dict:
        devices = SensorManager.get_user_devices(db, user_id)
        latest = None
        if devices:
            latest = SensorManager.get_latest_reading(db, user_id, devices[0].id)

        yield_improvement = []
        water_saving = []
        nutrient_optimization = []

        if latest:
            ph = latest.water_ph
            if ph < 5.5:
                nutrient_optimization.append({
                    "suggestion": "Gradually add pH-up buffer solution to raise pH to 6.0.",
                    "impact": "Improves nitrogen absorption, expected +8% harvest mass."
                })
            elif ph > 6.5:
                nutrient_optimization.append({
                    "suggestion": "Gradually add pH-down buffer solution to lower pH to 5.8.",
                    "impact": "Avoids iron lockout, preventing leaf chlorosis."
                })
            else:
                nutrient_optimization.append({
                    "suggestion": "Keep water pH stable at current level.",
                    "impact": "Optimal secondary macronutrient ingestion."
                })

            ec = latest.water_ec
            if ec > 2.2:
                nutrient_optimization.append({
                    "suggestion": "Dilute reservoir solution with RO water to lower EC.",
                    "impact": "Prevents tipburn and osmotic stress."
                })
            elif ec < 1.4:
                nutrient_optimization.append({
                    "suggestion": "Supplement nutrient solution to raise EC to 1.8 mS/cm.",
                    "impact": "Avoids nutrient deficiencies, expected +12% crop growth speed."
                })
            else:
                nutrient_optimization.append({
                    "suggestion": "Maintain EC stability at current value.",
                    "impact": "Ensures balanced N-P-K concentration."
                })

            temp = latest.temperature
            if temp > 26.0:
                yield_improvement.append({
                    "suggestion": "Increase exhaust ventilation speed or turn on cooling fan.",
                    "impact": "Reduces heat stress and transpiration load."
                })
            else:
                yield_improvement.append({
                    "suggestion": "Maintain air temperature setpoint at 21-24°C.",
                    "impact": "Optimal lettuce vegetative growth rate."
                })
        else:
            yield_improvement.append({
                "suggestion": "Keep grow room air temperature stable at 22°C.",
                "impact": "Maintains optimal leaf photosynthesis rate."
            })
            nutrient_optimization.append({
                "suggestion": "Formulate seedling water solution to target 1.5 mS/cm EC.",
                "impact": "Protects delicate root tissues from salt stress."
            })

        water_saving.append({
            "suggestion": "Implement pulse irrigation schedule during dark cycles.",
            "impact": "Reduces daily pump water consumption by up to 15%."
        })
        water_saving.append({
            "suggestion": "Insulate solution storage reservoir to reduce vaporization.",
            "impact": "Minimizes evaporative water loss."
        })

        return {
            "yield_improvement": yield_improvement,
            "water_saving": water_saving,
            "nutrient_optimization": nutrient_optimization
        }
