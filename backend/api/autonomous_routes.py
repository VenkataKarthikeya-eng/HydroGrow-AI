from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import FarmDecision, RecommendationHistory, AgentExecutionLog
from backend.services.decision_engine import DecisionEngine
from backend.services.automation.action_simulator import ActionSimulator
from backend.api.websocket_routes import ws_manager

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

class FeedbackInput(BaseModel):
    decision_id: int
    action_taken: str = Field(default="Reviewed action")
    feedback: str = Field(..., description="Helpful, Not Helpful, Completed, Ignored")

@router.get("/analyze", summary="Run multi-agent farm decision intelligence evaluation")
async def analyze_farm(
    db: Session = Depends(get_db), 
    user: Any = Depends(get_current_user_required)
):
    analysis_res = DecisionEngine.evaluate_farm_decisions(db, user.id)
    
    # Broadcast top recommendation via WebSocket if present
    if analysis_res["decisions"]:
        top_dec = analysis_res["decisions"][0]
        ws_payload = {
            "type": "ai_recommendation",
            "priority": top_dec["priority"],
            "title": top_dec["title"],
            "action": top_dec["recommended_action"],
            "confidence": top_dec["confidence_score"]
        }
        await ws_manager.broadcast_to_user(user.id, ws_payload)

    return analysis_res

@router.get("/decisions", summary="Get previous AI decisions log")
def get_decisions(
    db: Session = Depends(get_db), 
    user: Any = Depends(get_current_user_required)
):
    decisions = db.query(FarmDecision).filter(FarmDecision.user_id == user.id).order_by(FarmDecision.created_at.desc()).all()
    return [
        {
            "id": d.id,
            "decision_type": d.decision_type,
            "priority": d.priority,
            "title": d.title,
            "analysis": d.analysis,
            "recommended_action": d.recommended_action,
            "confidence_score": d.confidence_score,
            "status": d.status,
            "created_at": d.created_at.isoformat() if d.created_at else None
        }
        for d in decisions
    ]

@router.post("/execute/{decision_id}", summary="Execute decision action via simulator layer")
def execute_decision(
    decision_id: int, 
    db: Session = Depends(get_db), 
    user: Any = Depends(get_current_user_required)
):
    decision = db.query(FarmDecision).filter(FarmDecision.id == decision_id, FarmDecision.user_id == user.id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Farm decision not found.")

    # Interact with ActionSimulator layer
    target_device = "Nutrient Pump" if "EC" in decision.recommended_action or "Nutrient" in decision.recommended_action else "Cooling Fan"
    sim_res = ActionSimulator.simulate_action(
        device_name=target_device,
        action="activate",
        trigger_reason=f"Copilot Decision #{decision.id}: {decision.title}"
    )

    decision.status = "Executed"
    db.commit()

    return {
        "message": f"Successfully executed copilot action for Decision #{decision.id}",
        "decision_id": decision.id,
        "status": "Executed",
        "simulation_result": sim_res
    }

@router.post("/feedback", summary="Store farmer recommendation feedback")
def submit_feedback(
    data: FeedbackInput, 
    db: Session = Depends(get_db), 
    user: Any = Depends(get_current_user_required)
):
    decision = db.query(FarmDecision).filter(FarmDecision.id == data.decision_id, FarmDecision.user_id == user.id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Farm decision not found.")

    history_item = RecommendationHistory(
        user_id=user.id,
        decision_id=decision.id,
        action_taken=data.action_taken,
        feedback=data.feedback
    )
    db.add(history_item)

    if data.feedback in ["Completed", "Helpful"]:
        decision.status = "Executed"
    elif data.feedback == "Ignored":
        decision.status = "Dismissed"

    db.commit()

    return {
        "message": "Feedback logged successfully.",
        "decision_id": decision.id,
        "feedback": data.feedback
    }
