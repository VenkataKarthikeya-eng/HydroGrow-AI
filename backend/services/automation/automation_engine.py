from sqlalchemy.orm import Session
from backend.database.models import AutomationRule, AutomationEvent
from backend.services.automation.action_simulator import ActionSimulator

class AutomationEngine:
    """
    Evaluates telemetry readings against active user automation rules,
    triggering simulated actuator states and saving executed events to DB.
    """
    @staticmethod
    def evaluate_condition(value: float, condition: str, threshold: float) -> bool:
        if condition == "above":
            return value > threshold
        elif condition == "below":
            return value < threshold
        return False

    @staticmethod
    def process_sensor_update(
        db: Session, 
        user_id: int, 
        reading_id: int, 
        reading_data: dict
    ) -> list:
        rules = db.query(AutomationRule).filter(
            AutomationRule.user_id == user_id,
            AutomationRule.enabled == True
        ).all()

        triggered_events = []

        for rule in rules:
            param_key = rule.parameter
            if param_key not in reading_data:
                continue

            current_val = float(reading_data[param_key])
            is_matched = AutomationEngine.evaluate_condition(
                current_val, 
                rule.condition, 
                rule.threshold_value
            )

            if is_matched:
                sim_res = ActionSimulator.simulate_action(
                    rule.action_value,
                    rule.action_type,
                    rule.rule_name
                )

                msg = f"Rule [{rule.rule_name}] triggered. {rule.action_value} was {sim_res['status']}."
                event = AutomationEvent(
                    user_id=user_id,
                    rule_id=rule.id,
                    sensor_reading_id=reading_id,
                    event_type="device_actuation",
                    message=msg,
                    status="executed"
                )
                db.add(event)
                db.commit()
                db.refresh(event)

                triggered_events.append({
                    "id": event.id,
                    "rule_id": rule.id,
                    "device": rule.action_value,
                    "status": sim_res["status"],
                    "message": msg,
                    "created_at": event.created_at.isoformat() if event.created_at else None
                })

        return triggered_events
