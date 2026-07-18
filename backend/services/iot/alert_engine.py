from sqlalchemy.orm import Session
from backend.database.models import Alert

class AlertEngine:
    """
    Evaluates environmental inputs against critical thresholds and moving
    averages to generate farm alerts and register them in the database.
    """
    @staticmethod
    def analyze_readings_for_alerts(
        db: Session, 
        user_id: int, 
        reading: dict, 
        averages: dict
    ) -> list:
        alerts = []

        ph = float(reading.get("water_ph", 6.0))
        if ph < 5.0 or ph > 7.0:
            alerts.append({
                "alert_type": "water_ph",
                "severity": "critical",
                "parameter": "Water pH",
                "message": f"Critical: pH level is dangerously skewed at {ph}."
            })
        elif ph < 5.5 or ph > 6.5:
            alerts.append({
                "alert_type": "water_ph",
                "severity": "warning",
                "parameter": "Water pH",
                "message": f"Warning: pH level {ph} has drifted outside optimal 5.5-6.5 boundaries."
            })

        temp = float(reading.get("temperature", 22.0))
        if temp > 30.0:
            alerts.append({
                "alert_type": "temperature",
                "severity": "critical",
                "parameter": "Air Temperature",
                "message": f"Critical: High room temperature detected ({temp}°C)."
            })
        elif temp > 26.0 or temp < 18.0:
            alerts.append({
                "alert_type": "temperature",
                "severity": "warning",
                "parameter": "Air Temperature",
                "message": f"Warning: Room temperature {temp}°C is slightly stressful."
            })

        ec = float(reading.get("water_ec", 1.8))
        if ec > 3.0:
            alerts.append({
                "alert_type": "water_ec",
                "severity": "critical",
                "parameter": "Water EC",
                "message": f"Critical: Electrical Conductivity {ec} mS/cm is extremely concentrated."
            })
        elif ec > 2.5 or ec < 1.2:
            alerts.append({
                "alert_type": "water_ec",
                "severity": "warning",
                "parameter": "Water EC",
                "message": f"Warning: Nutrient solution EC {ec} mS/cm is outside optimal targets."
            })

        hum = float(reading.get("humidity", 60.0))
        if hum > 85.0 or hum < 40.0:
            alerts.append({
                "alert_type": "humidity",
                "severity": "critical",
                "parameter": "Humidity",
                "message": f"Critical: Extreme relative humidity detected ({hum}%)."
            })
        elif hum > 75.0 or hum < 45.0:
            alerts.append({
                "alert_type": "humidity",
                "severity": "warning",
                "parameter": "Humidity",
                "message": f"Warning: Grow room humidity {hum}% is slightly out of bounds."
            })

        for a in alerts:
            db_alert = Alert(
                user_id=user_id,
                alert_type=a["alert_type"],
                severity=a["severity"],
                parameter=a["parameter"],
                message=a["message"],
                resolved=False
            )
            db.add(db_alert)
        db.commit()

        return alerts
