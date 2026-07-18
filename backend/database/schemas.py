import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime.datetime

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

class PredictionHistoryResponse(BaseModel):
    id: int
    user_id: int
    crop_type: str
    input_parameters: Dict[str, Any]
    predicted_weight: float
    growth_category: str
    recommendations: Optional[List[Dict[str, Any]]] = None
    explanation: Optional[Dict[str, Any]] = None
    created_at: datetime.datetime

    model_config = {
        "from_attributes": True
    }

class ConversationCreate(BaseModel):
    title: str = Field(..., min_length=1)

class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime.datetime

    model_config = {
        "from_attributes": True
    }

class MessageCreate(BaseModel):
    role: str
    content: str
    sources: Optional[List[str]] = None

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    sources: Optional[List[str]] = None
    created_at: datetime.datetime

    model_config = {
        "from_attributes": True
    }
