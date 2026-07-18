from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.database import models, crud

class MemoryManager:
    """
    Manages loading and saving conversation messages and prediction logs
    from the database persistence layer.
    """
    @staticmethod
    def get_user_conversations(db: Session, user_id: int) -> List[models.Conversation]:
        return crud.get_conversations_by_user_id(db, user_id)

    @staticmethod
    def get_conversation_messages(db: Session, conversation_id: int) -> List[models.Message]:
        return crud.get_messages_by_conversation_id(db, conversation_id)

    @staticmethod
    def get_user_predictions(db: Session, user_id: int) -> List[models.Prediction]:
        return crud.get_predictions_by_user_id(db, user_id)

    @staticmethod
    def get_latest_prediction(db: Session, user_id: int) -> Optional[models.Prediction]:
        predictions = crud.get_predictions_by_user_id(db, user_id)
        return predictions[0] if predictions else None

    @staticmethod
    def save_message(
        db: Session, 
        conversation_id: int, 
        role: str, 
        content: str, 
        sources: Optional[list] = None
    ) -> models.Message:
        return crud.create_message(db, conversation_id, role, content, sources)

    @staticmethod
    def save_prediction(
        db: Session, 
        user_id: int, 
        input_parameters: dict, 
        predicted_weight: float, 
        growth_category: str,
        recommendations: Optional[list] = None,
        explanation: Optional[dict] = None
    ) -> models.Prediction:
        return crud.create_prediction(
            db, 
            user_id, 
            input_parameters, 
            predicted_weight, 
            growth_category, 
            recommendations, 
            explanation
        )
