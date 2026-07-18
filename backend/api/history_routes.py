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
