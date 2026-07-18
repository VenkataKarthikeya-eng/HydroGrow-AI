from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.database.models import Prediction

class AnomalyDetector:
    """
    Scans historic user prediction logs to detect sudden crop yield drops,
    abnormal grow-room parameters, and recurrent parameter warning alerts.
    """
    @staticmethod
    def detect_anomalies(db: Session, user_id: int) -> List[Dict[str, Any]]:
        predictions = (
            db.query(Prediction)
            .filter(Prediction.user_id == user_id)
            .order_by(Prediction.created_at.asc())
            .all()
        )
        
        alerts = []
        if not predictions:
            return alerts

        # 1. Sudden yield drops (>20% decline)
        weights = [p.predicted_weight for p in predictions]
        if len(weights) >= 2:
            prev = weights[-2]
            curr = weights[-1]
            if prev > 0 and ((prev - curr) / prev) > 0.20:
                alerts.append({
                    "alert": "Sudden yield drop detected",
                    "reason": f"Harvest weight dropped from {prev:.1f}g to {curr:.1f}g (a decline of {round(((prev - curr)/prev)*100, 1)}%) in consecutive cycles.",
                    "severity": "critical"
                })

        # 2. Abnormal parameter checks on the latest prediction
        latest_pred = predictions[-1]
        params = latest_pred.input_parameters or {}
        
        air_temp = float(params.get("air_temperature", 22.0))
        if air_temp > 28.0 or air_temp < 15.0:
            alerts.append({
                "alert": "Abnormal grow room temperature",
                "reason": f"Active grow room air temperature ({air_temp}°C) deviates heavily from ideal lettuce growth temperatures.",
                "severity": "warning"
            })
            
        ph = float(params.get("water_ph", 6.0))
        if ph > 7.0 or ph < 5.0:
            alerts.append({
                "alert": "Dangerous water pH level",
                "reason": f"Active solution acidity pH ({ph}) locks out macronutrient absorption paths.",
                "severity": "critical"
            })

        # 3. Repeated critical warnings count
        recs_with_warnings = 0
        for p in reversed(predictions[-3:]):
            recs = p.recommendations or []
            if any(r.get("status") in ["Critical", "Warning"] for r in recs if isinstance(r, dict)):
                recs_with_warnings += 1

        if recs_with_warnings >= 3:
            alerts.append({
                "alert": "Persistent environmental issues",
                "reason": "Warning environmental parameters detected in 3 consecutive crop cycles. Adjust dosing systems.",
                "severity": "warning"
            })

        return alerts
