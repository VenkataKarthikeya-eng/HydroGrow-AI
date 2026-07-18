import time
import asyncio
from sqlalchemy.orm import Session
from backend.database.models import (
    FarmDecision, AgentExecutionLog, RecommendationHistory,
    SensorReading, SensorDevice, PlantAnalysis, PlantImage,
    CropCycle, Prediction, SimulationRun, DigitalTwinProfile
)
from backend.services.ai_agents.crop_agent import CropAgent
from backend.services.ai_agents.climate_agent import ClimateAgent
from backend.services.ai_agents.disease_agent import DiseaseAgent
from backend.services.ai_agents.nutrition_agent import NutritionAgent
from backend.services.ai_agents.optimization_agent import OptimizationAgent

PRIORITY_ORDER = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}

class DecisionEngine:
    """
    Multi-Agent Decision Intelligence Harvester & Priority Ranker.
    Synthesizes telemetry across IoT, Vision, Digital Twin, and Analytics.
    """

    @staticmethod
    def collect_context(db: Session, user_id: int) -> dict:
        context = {
            "iot_info": {},
            "vision_info": {},
            "crop_info": {},
            "prediction_info": {},
            "digital_twin": {}
        }

        # 1. IoT telemetry
        latest_iot = (
            db.query(SensorReading)
            .join(SensorDevice)
            .filter(SensorDevice.user_id == user_id)
            .order_by(SensorReading.timestamp.desc())
            .first()
        )
        if latest_iot:
            context["iot_info"] = {
                "temperature": latest_iot.temperature,
                "humidity": latest_iot.humidity,
                "water_ph": latest_iot.water_ph,
                "water_ec": latest_iot.water_ec,
                "water_temperature": latest_iot.water_temperature,
                "co2": latest_iot.co2,
                "nutrient_level": latest_iot.nutrient_level
            }

        # 2. Vision pathology scan
        latest_vision = (
            db.query(PlantAnalysis)
            .join(PlantImage)
            .filter(PlantImage.user_id == user_id)
            .order_by(PlantAnalysis.created_at.desc())
            .first()
        )
        if latest_vision:
            context["vision_info"] = {
                "health_score": latest_vision.health_score,
                "disease": latest_vision.disease_name,
                "confidence": latest_vision.confidence_score,
                "severity": latest_vision.severity,
                "recommendations": latest_vision.recommendations
            }

        # 3. Crop Cycle
        latest_crop = (
            db.query(CropCycle)
            .filter(CropCycle.user_id == user_id)
            .order_by(CropCycle.start_date.desc())
            .first()
        )
        if latest_crop:
            context["crop_info"] = {
                "crop_name": latest_crop.crop_name,
                "current_stage": latest_crop.current_stage,
                "growth_progress": latest_crop.growth_progress,
                "days_remaining": latest_crop.days_remaining
            }

        # 4. Predictions
        latest_pred = (
            db.query(Prediction)
            .filter(Prediction.user_id == user_id)
            .order_by(Prediction.created_at.desc())
            .first()
        )
        if latest_pred:
            context["prediction_info"] = {
                "predicted_weight": latest_pred.predicted_weight,
                "growth_category": latest_pred.growth_category
            }

        # 5. Digital Twin
        latest_twin = (
            db.query(SimulationRun)
            .filter(SimulationRun.user_id == user_id)
            .order_by(SimulationRun.created_at.desc())
            .first()
        )
        if latest_twin:
            context["digital_twin"] = {
                "scenario_name": latest_twin.scenario_name,
                "yield_change_percentage": latest_twin.yield_change_percentage,
                "final_prediction": latest_twin.final_prediction
            }

        return context

    @staticmethod
    def run_multi_agents(context: dict) -> list:
        results = []
        
        # Execute sub-agents
        crop_res = CropAgent.run(context)
        results.append(crop_res)

        climate_res = ClimateAgent.run(context)
        results.append(climate_res)

        disease_res = DiseaseAgent.run(context)
        results.append(disease_res)

        nutrition_res = NutritionAgent.run(context)
        results.append(nutrition_res)

        opt_res = OptimizationAgent.run(context, results)
        results.append(opt_res)

        return results

    @staticmethod
    def deduplicate_and_rank(results: list) -> list:
        # Merge overlapping actions or titles
        seen_actions = set()
        merged = []
        
        for res in results:
            action_key = res["recommended_action"].strip().lower()
            if action_key in seen_actions:
                continue
            seen_actions.add(action_key)
            merged.append(res)

        # Sort by Priority (CRITICAL > HIGH > MEDIUM > LOW) then Confidence Score
        sorted_results = sorted(
            merged,
            key=lambda x: (PRIORITY_ORDER.get(x["priority"], 1), x["confidence_score"]),
            reverse=True
        )
        return sorted_results

    @staticmethod
    def calculate_farm_health_score(context: dict, ranked_results: list) -> float:
        base_health = 100.0
        
        # Deduct based on active priorities
        for res in ranked_results:
            prio = res.get("priority")
            if prio == "CRITICAL":
                base_health -= 25.0
            elif prio == "HIGH":
                base_health -= 12.0
            elif prio == "MEDIUM":
                base_health -= 5.0

        # Incorporate vision health score if available
        vision_score = context.get("vision_info", {}).get("health_score")
        if vision_score is not None:
            base_health = (base_health * 0.6) + (vision_score * 0.4)

        return round(max(0.0, min(100.0, base_health)), 1)

    @classmethod
    def evaluate_farm_decisions(cls, db: Session, user_id: int) -> dict:
        t0 = time.time()
        context = cls.collect_context(db, user_id)
        raw_agent_results = cls.run_multi_agents(context)
        exec_duration = round(time.time() - t0, 3)

        # Log agent executions to DB
        for res in raw_agent_results:
            log_item = AgentExecutionLog(
                user_id=user_id,
                agent_name=res["agent_name"],
                input_context=context,
                output_result=res,
                execution_time=exec_duration
            )
            db.add(log_item)

        ranked = cls.deduplicate_and_rank(raw_agent_results)
        farm_health = cls.calculate_farm_health_score(context, ranked)

        # Save decisions to DB
        saved_decisions = []
        for dec in ranked:
            db_decision = FarmDecision(
                user_id=user_id,
                decision_type=dec["decision_type"],
                priority=dec["priority"],
                title=dec["title"],
                analysis=dec["analysis"],
                recommended_action=dec["recommended_action"],
                confidence_score=dec["confidence_score"],
                status="Pending"
            )
            db.add(db_decision)
            saved_decisions.append(db_decision)

        db.commit()

        # Format output
        active_issues_count = sum(1 for d in ranked if d["priority"] in ["CRITICAL", "HIGH", "MEDIUM"])

        return {
            "farm_health": farm_health,
            "active_issues_count": active_issues_count,
            "agent_statuses": [
                {
                    "agent_name": r["agent_name"],
                    "status": "Optimal" if r["priority"] == "LOW" else "Alert",
                    "priority": r["priority"]
                }
                for r in raw_agent_results
            ],
            "decisions": [
                {
                    "id": d.id if hasattr(d, "id") else None,
                    "decision_type": dec["decision_type"],
                    "priority": dec["priority"],
                    "title": dec["title"],
                    "analysis": dec["analysis"],
                    "recommended_action": dec["recommended_action"],
                    "confidence_score": dec["confidence_score"],
                    "affected_parameters": dec.get("affected_parameters", []),
                    "status": "Pending"
                }
                for d, dec in zip(saved_decisions, ranked)
            ]
        }
