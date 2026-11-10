from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.database import crud, schemas, models
from backend.authentication.jwt_handler import get_current_user

router = APIRouter(prefix="/api/history", tags=["History"])

@router.get("/predictions", response_model=List[schemas.PredictionHistoryResponse], summary="Retrieve grower prediction logs")
def get_prediction_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_predictions_by_user_id(db, user_id=current_user.id)

@router.post("/predictions", summary="Save a prediction to grower history")
def save_prediction_history(
    payload: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    input_params = payload.get("input_parameters") or payload.get("inputs") or {}
    weight = float(payload.get("predicted_weight") or payload.get("predicted_yield_grams") or 0.0)
    category = str(payload.get("growth_category") or payload.get("status") or "Optimal Growth")
    recs = payload.get("recommendations") or []
    expl = payload.get("explanation") or {}

    pred = crud.create_prediction(
        db=db,
        user_id=current_user.id,
        input_parameters=input_params,
        predicted_weight=weight,
        growth_category=category,
        recommendations=recs if isinstance(recs, list) else [recs],
        explanation=expl if isinstance(expl, dict) else {}
    )
    return {
        "status": "success",
        "id": pred.id,
        "user_id": pred.user_id,
        "predicted_weight": pred.predicted_weight,
        "growth_category": pred.growth_category,
        "created_at": pred.created_at.isoformat() if pred.created_at else None
    }

@router.get("/chats", response_model=List[schemas.ConversationResponse], summary="Retrieve grower chat conversations")
def get_chat_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_conversations_by_user_id(db, user_id=current_user.id)

@router.get("/chats/{conversation_id}", response_model=List[schemas.MessageResponse], summary="Retrieve messages in a conversation")
def get_conversation_messages(
    conversation_id: int, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    conversation = crud.get_conversation(db, conversation_id=conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this conversation"
        )
    return crud.get_messages_by_conversation_id(db, conversation_id=conversation_id)

@router.post("/chats", response_model=schemas.ConversationResponse, summary="Create a new conversation thread")
def create_new_conversation(
    conv_data: schemas.ConversationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_conversation(db, user_id=current_user.id, title=conv_data.title)
