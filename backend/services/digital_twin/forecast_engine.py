from datetime import datetime, timedelta
from backend.services.digital_twin.growth_simulator import GrowthSimulator

class ForecastEngine:
    """
    Simulates crop growth curve projections and estimates harvest calendars.
    """
    @staticmethod
    def generate_growth_forecast(conditions: dict, duration_days: int = 35) -> dict:
        forecast_days = []
        for d in range(1, duration_days + 1):
            day_state = GrowthSimulator.calculate_daily_state(d, conditions)
            forecast_days.append(day_state)
            
        final_state = forecast_days[-1]
        
        expected_weight = final_state["predicted_weight"]
        confidence = 0.95
        
        temp = conditions.get("temperature", 22.0)
        ec = conditions.get("water_ec", 2.0)
        if abs(temp - 22.0) > 5.0 or abs(ec - 2.0) > 0.6:
            confidence -= 0.15
            
        expected_harvest_date = (datetime.utcnow() + timedelta(days=duration_days)).date().isoformat()
        
        risks = []
        if temp > 28.0:
            risks.append("Tip Burn risk is high due to thermal leaf transpiration lockout.")
        if ec < 1.2:
            risks.append("Nutrient starvation risks stunting vegetative growth.")
        if ec > 2.8:
            risks.append("Excess nutrients EC risks leaf tip burn necrosis.")
            
        return {
            "growth_forecast": forecast_days,
            "expected_harvest_weight": expected_weight,
            "expected_harvest_date": expected_harvest_date,
            "confidence_score": round(confidence, 2),
            "risk_factors": risks
        }
