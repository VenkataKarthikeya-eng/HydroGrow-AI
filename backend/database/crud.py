from typing import List, Optional
from sqlalchemy.orm import Session
from backend.database import models, schemas

# User operations
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, password_hash: str) -> models.User:
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=password_hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Prediction operations
def create_prediction(
    db: Session, 
    user_id: int, 
    input_parameters: dict, 
    predicted_weight: float, 
    growth_category: str,
    recommendations: Optional[list] = None,
    explanation: Optional[dict] = None
) -> models.Prediction:
    db_pred = models.Prediction(
        user_id=user_id,
        input_parameters=input_parameters,
        predicted_weight=predicted_weight,
        growth_category=growth_category,
        recommendations=recommendations,
        explanation=explanation
    )
    db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred

def get_predictions_by_user_id(db: Session, user_id: int) -> List[models.Prediction]:
    return db.query(models.Prediction).filter(models.Prediction.user_id == user_id).order_by(models.Prediction.created_at.desc()).all()

# Chat operations
def create_conversation(db: Session, user_id: int, title: str) -> models.Conversation:
    db_conv = models.Conversation(
        user_id=user_id,
        title=title
    )
    db.add(db_conv)
    db.commit()
    db.refresh(db_conv)
    return db_conv

def get_conversations_by_user_id(db: Session, user_id: int) -> List[models.Conversation]:
    return db.query(models.Conversation).filter(models.Conversation.user_id == user_id).order_by(models.Conversation.created_at.desc()).all()

def get_conversation(db: Session, conversation_id: int) -> Optional[models.Conversation]:
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def create_message(
    db: Session, 
    conversation_id: int, 
    role: str, 
    content: str, 
    sources: Optional[list] = None
) -> models.Message:
    db_msg = models.Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        sources=sources
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

def get_messages_by_conversation_id(db: Session, conversation_id: int) -> List[models.Message]:
    return db.query(models.Message).filter(models.Message.conversation_id == conversation_id).order_by(models.Message.created_at.asc()).all()
