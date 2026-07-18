from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from backend.database.models import Prediction

class AnalyticsEngine:
    """
    Main engine for aggregating user statistics, prediction summaries,
    and average environment variables from the database.
    """
    @staticmethod
    def get_user_statistics(db: Session, user_id: int) -> Dict[str, Any]:
        total = db.query(func.count(Prediction.id)).filter(Prediction.user_id == user_id).scalar() or 0
        if total == 0:
            return {
                "total_predictions": 0,
                "average_weight": 0.0,
                "best_prediction": 0.0,
                "success_rate": 0.0
            }

        avg_weight = db.query(func.avg(Prediction.predicted_weight)).filter(Prediction.user_id == user_id).scalar() or 0.0
        best_weight = db.query(func.max(Prediction.predicted_weight)).filter(Prediction.user_id == user_id).scalar() or 0.0
        successful = db.query(func.count(Prediction.id)).filter(
            Prediction.user_id == user_id, 
            Prediction.growth_category != "Poor"
        ).scalar() or 0

        success_rate = round((successful / total) * 100.0, 1)
        return {
            "total_predictions": total,
            "average_weight": round(avg_weight, 1),
            "best_prediction": round(best_weight, 1),
            "success_rate": success_rate
        }

    @staticmethod
    def get_prediction_summary(db: Session, user_id: int) -> List[Dict[str, Any]]:
        # Timeseries list of predictions
        predictions = (
            db.query(Prediction)
            .filter(Prediction.user_id == user_id)
            .order_by(Prediction.created_at.asc())
            .all()
        )
        return [
            {
                "id": p.id,
                "date": p.created_at.strftime("%Y-%m-%d") if p.created_at else "N/A",
                "weight": round(p.predicted_weight, 1),
                "category": p.growth_category
            }
            for p in predictions
        ]

    @staticmethod
    def get_environment_statistics(db: Session, user_id: int) -> Dict[str, Any]:
        # Fetch just the parameters json column from database in one query
        records = [
            r[0] for r in db.query(Prediction.input_parameters)
            .filter(Prediction.user_id == user_id)
            .all() if r[0]
        ]
        
        total = len(records)
        if total == 0:
            return {
                "water_ph": {"avg": 0.0, "min": 0.0, "max": 0.0},
                "water_ec": {"avg": 0.0, "min": 0.0, "max": 0.0},
                "air_temperature": {"avg": 0.0, "min": 0.0, "max": 0.0},
                "humidity": {"avg": 0.0, "min": 0.0, "max": 0.0},
                "co2": {"avg": 0.0, "min": 0.0, "max": 0.0},
                "water_temperature": {"avg": 0.0, "min": 0.0, "max": 0.0}
            }

        keys = ["water_ph", "water_ec", "air_temperature", "humidity", "co2", "water_temperature"]
        stats = {}
        for key in keys:
            vals = [float(r.get(key, 0.0)) for r in records if key in r]
            if not vals:
                vals = [0.0]
            stats[key] = {
                "avg": round(sum(vals) / len(vals), 2),
                "min": round(min(vals), 2),
                "max": round(max(vals), 2)
            }
        return stats

    @staticmethod
    def get_growth_performance(db: Session, user_id: int) -> List[Dict[str, Any]]:
        # Group category percentage calculator
        total = db.query(func.count(Prediction.id)).filter(Prediction.user_id == user_id).scalar() or 0
        if total == 0:
            return []

        categories = (
            db.query(Prediction.growth_category, func.count(Prediction.id))
            .filter(Prediction.user_id == user_id)
            .group_by(Prediction.growth_category)
            .all()
        )
        return [
            {
                "category": cat,
                "count": count,
                "percentage": round((count / total) * 100, 1)
            }
            for cat, count in categories
        ]
