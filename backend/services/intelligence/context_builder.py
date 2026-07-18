from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.database import crud
from backend.services.intelligence.memory_manager import MemoryManager

class ContextBuilder:
    """
    Constructs context objects (user profiles, prediction context, conversation history)
    to augment prompt payloads and intent detections.
    """
    @staticmethod
    def build_user_context(user_id: Optional[int], db: Session) -> Dict[str, Any]:
        if not user_id:
            return {
                "authenticated": False,
                "role": "Anonymous Grower",
                "greenhouse_id": "GH-Alpha-01"
            }
        user = crud.get_user(db, user_id)
        if not user:
            return {
                "authenticated": False,
                "role": "Anonymous Grower",
                "greenhouse_id": "GH-Alpha-01"
            }
        return {
            "authenticated": True,
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": "Head Grower",
            "greenhouse_id": "GH-Alpha-01"
        }

    @staticmethod
    def build_prediction_context(user_id: Optional[int], db: Session) -> Dict[str, Any]:
        if not user_id:
            return {}
        latest = MemoryManager.get_latest_prediction(db, user_id)
        if not latest:
            return {}
        return {
            "predicted_weight": latest.predicted_weight,
            "growth_category": latest.growth_category,
            "input_parameters": latest.input_parameters,
            "recommendations": latest.recommendations,
            "explanation": latest.explanation,
            "created_at": latest.created_at.isoformat() if latest.created_at else None
        }

    @staticmethod
    def build_conversation_context(conversation_id: Optional[int], db: Session) -> list:
        if not conversation_id:
            return []
        messages = MemoryManager.get_conversation_messages(db, conversation_id)
        # Format as conversation history list expected by assistant
        return [{"role": m.role, "content": m.content} for m in messages]
