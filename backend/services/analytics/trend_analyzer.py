import math
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.database.models import Prediction

def pearson_correlation(x: List[float], y: List[float]) -> float:
    n = len(x)
    if n < 2:
        return 0.0
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_sq = sum(val**2 for val in x)
    sum_y_sq = sum(val**2 for val in y)
    sum_p_xy = sum(x[i] * y[i] for i in range(n))
    
    num = (n * sum_p_xy) - (sum_x * sum_y)
    den = ((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2))**0.5
    if den == 0:
        return 0.0
    return round(num / den, 2)

class TrendAnalyzer:
    """
    Computes Pearson correlation coefficients and trends between environmental
    parameters and harvest weights.
    """
    @staticmethod
    def get_parameter_trends(db: Session, user_id: int) -> Dict[str, Any]:
        predictions = (
            db.query(Prediction)
            .filter(Prediction.user_id == user_id)
            .order_by(Prediction.created_at.asc())
            .all()
        )
        if not predictions:
            return {}

        weights = [float(p.predicted_weight) for p in predictions]
        
        ph_vals = []
        ec_vals = []
        temp_vals = []
        humidity_vals = []
        nutrient_vals = []
        water_vals = []

        for p in predictions:
            params = p.input_parameters or {}
            ph_vals.append(float(params.get("water_ph", 6.0)))
            ec_vals.append(float(params.get("water_ec", 2.0)))
            temp_vals.append(float(params.get("air_temperature", 22.0)))
            humidity_vals.append(float(params.get("humidity", 60.0)))
            nutrient_vals.append(float(params.get("nutrient_solution_ml", 400.0)))
            water_vals.append(float(params.get("water_consumption_l", 170.0)))

        trends = {
            "air_temperature": {
                "correlation": pearson_correlation(temp_vals, weights),
                "optimal_range": "20.0-24.0°C",
                "impact": "positive" if pearson_correlation(temp_vals, weights) >= 0 else "negative"
            },
            "humidity": {
                "correlation": pearson_correlation(humidity_vals, weights),
                "optimal_range": "50.0-70.0%",
                "impact": "positive" if pearson_correlation(humidity_vals, weights) >= 0 else "negative"
            },
            "water_ph": {
                "correlation": pearson_correlation(ph_vals, weights),
                "optimal_range": "5.5-6.5",
                "impact": "positive" if pearson_correlation(ph_vals, weights) >= 0 else "negative"
            },
            "water_ec": {
                "correlation": pearson_correlation(ec_vals, weights),
                "optimal_range": "1.5-2.5 mS/cm",
                "impact": "positive" if pearson_correlation(ec_vals, weights) >= 0 else "negative"
            },
            "nutrient_solution_ml": {
                "correlation": pearson_correlation(nutrient_vals, weights),
                "optimal_range": "300.0-500.0 mL",
                "impact": "positive" if pearson_correlation(nutrient_vals, weights) >= 0 else "negative"
            },
            "water_consumption_l": {
                "correlation": pearson_correlation(water_vals, weights),
                "optimal_range": "150.0-200.0 L",
                "impact": "positive" if pearson_correlation(water_vals, weights) >= 0 else "negative"
            }
        }
        return trends
