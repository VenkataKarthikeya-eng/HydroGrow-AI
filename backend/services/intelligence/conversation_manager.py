import re
import datetime
from typing import Optional
from sqlalchemy.orm import Session
from backend.database import models

class ConversationManager:
    """
    Manages agricultural conversation thread titles and metadata updates,
    such as message counting and last message timestamps.
    """
    @staticmethod
    def generate_conversation_title(message: str) -> str:
        # Rule-based classification for auto-generating conversation titles
        clean_msg = message.lower().strip()
        
        # Check parameters
        if re.search(r'\b(ph|acidity|alkalinity)\b', clean_msg):
            return "Water pH Adjustment"
        if re.search(r'\b(ec|electrical conductivity|tds|nutrient level|parts per million|ppm)\b', clean_msg):
            return "Nutrient EC Management"
        if re.search(r'\b(temp|temperature|heat|cold|warm)\b', clean_msg):
            return "Grow Room Temperature Control"
        if re.search(r'\b(humidity|rh|moisture|air moisture)\b', clean_msg):
            return "Humidity & VPD Optimization"
        if re.search(r'\b(co2|carbon dioxide)\b', clean_msg):
            return "CO2 Dosing Optimization"
            
        # Check problems
        if re.search(r'\b(pythium|root rot|brown roots|slime)\b', clean_msg):
            return "Pythium Root Rot Diagnosis"
        if re.search(r'\b(tipburn|tip burn|edge burn|dieback)\b', clean_msg):
            return "Tipburn Deficiency Issues"
        if re.search(r'\b(yellow|chlorosis|pale leaves)\b', clean_msg):
            return "Yellow Leaf Chlorosis Analysis"
            
        # Check prediction/yield
        if re.search(r'\b(prediction|yield|predicted weight|harvest weight|size)\b', clean_msg):
            return "Crop Prediction Diagnostic"
            
        # Default fallback: grab first 4-5 words
        words = [w.capitalize() for w in message.split()[:4]]
        if not words:
            return "New Chat Thread"
        return " ".join(words) + ("..." if len(message.split()) > 4 else "")

    @classmethod
    def update_conversation_metadata(
        cls, 
        db: Session, 
        conversation_id: int, 
        new_message_content: Optional[str] = None
    ) -> Optional[models.Conversation]:
        conv = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
        if not conv:
            return None
            
        # Update message count
        msg_count = db.query(models.Message).filter(models.Message.conversation_id == conversation_id).count()
        conv.message_count = msg_count
        conv.last_message_time = datetime.datetime.utcnow()
        
        # If it's the first user message, generate title automatically
        if msg_count == 1 and new_message_content:
            conv.title = cls.generate_conversation_title(new_message_content)
        elif (conv.title == "New grow room query" or conv.title.startswith("Chat Session")) and new_message_content:
            # Override default initial thread title
            conv.title = cls.generate_conversation_title(new_message_content)
            
        db.commit()
        db.refresh(conv)
        return conv
