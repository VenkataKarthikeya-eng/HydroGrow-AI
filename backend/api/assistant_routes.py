import re
import json
import asyncio
from typing import Optional, Any
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from backend.services.intelligence.ai_assistant import HydroGrowAssistant
from backend.services.intelligence.intent_classifier import IntentClassifier
from backend.services.intelligence.conversation_manager import ConversationManager
from backend.services.intelligence.context_builder import ContextBuilder
from backend.services.prediction.prediction import predict
from backend.services.intelligence.recommendation_engine import generate_recommendations
from backend.services.intelligence.explanation_engine import generate_explanation
from backend.rag.retriever import retrieve
from backend.database.connection import get_db
from backend.database import crud
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import PlantAnalysis, PlantImage, Prediction, SensorReading, SensorDevice, SimulationRun, DigitalTwinProfile, FarmDecision

def compile_vision_and_farm_contexts(db: Session, user_id: int) -> dict:
    vision_context = {}
    prediction_context = {}
    iot_context = {}
    twin_context = {}
    copilot_context = []
    
    # Latest decisions
    latest_decisions = (
        db.query(FarmDecision)
        .filter(FarmDecision.user_id == user_id)
        .order_by(FarmDecision.created_at.desc())
        .limit(5)
        .all()
    )
    if latest_decisions:
        copilot_context = [
            {
                "title": d.title,
                "priority": d.priority,
                "type": d.decision_type,
                "analysis": d.analysis,
                "action": d.recommended_action,
                "confidence": d.confidence_score
            }
            for d in latest_decisions
        ]
    
    # Latest simulation
    latest_sim = (
        db.query(SimulationRun)
        .filter(SimulationRun.user_id == user_id)
        .order_by(SimulationRun.created_at.desc())
        .first()
    )
    if latest_sim:
        twin_context = {
            "scenario_name": latest_sim.scenario_name,
            "duration_days": latest_sim.duration_days,
            "final_prediction": latest_sim.final_prediction,
            "yield_change_percentage": latest_sim.yield_change_percentage,
            "initial_conditions": latest_sim.initial_conditions
        }
    
    latest_scan = (
        db.query(PlantAnalysis)
        .join(PlantImage)
        .filter(PlantImage.user_id == user_id)
        .order_by(PlantAnalysis.created_at.desc())
        .first()
    )
    if latest_scan:
        vision_context = {
            "health_score": latest_scan.health_score,
            "disease": latest_scan.disease_name,
            "confidence": latest_scan.confidence_score,
            "severity": latest_scan.severity,
            "growth_stage": latest_scan.image.growth_stage,
            "recommendations": latest_scan.recommendations
        }
        
    latest_pred = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .first()
    )
    if latest_pred:
        prediction_context = {
            "predicted_weight": latest_pred.predicted_weight,
            "growth_category": latest_pred.growth_category,
            "input_parameters": latest_pred.input_parameters
        }
        
    latest_reading = (
        db.query(SensorReading)
        .join(SensorDevice)
        .filter(SensorDevice.user_id == user_id)
        .order_by(SensorReading.timestamp.desc())
        .first()
    )
    if latest_reading:
        iot_context = {
            "temperature": latest_reading.temperature,
            "humidity": latest_reading.humidity,
            "water_ph": latest_reading.water_ph,
            "water_ec": latest_reading.water_ec,
            "water_temperature": latest_reading.water_temperature,
            "co2": latest_reading.co2,
            "nutrient_level": latest_reading.nutrient_level
        }
        
    return {
        "vision_context": vision_context,
        "prediction_context": prediction_context,
        "iot_context": iot_context,
        "digital_twin": twin_context,
        "copilot_decisions": copilot_context
    }

router = APIRouter()

# Instantiate the assistant as a singleton
assistant = HydroGrowAssistant()

class ChatInput(BaseModel):
    message: str = Field(..., description="The query/question typed by the grower")
    conversation_history: list = Field(default=[], description="List of previous conversation messages")
    context: dict = Field(default={}, description="Current dashboard state context (inputs, prediction, etc.)")
    conversation_id: Optional[int] = Field(default=None, description="Optional DB conversation thread ID")

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Why is my prediction only 245g?",
                "conversation_history": [
                    {"role": "user", "content": "How can I improve my lettuce yield?"},
                    {"role": "assistant", "content": "Keep water pH optimal (5.5-6.5)..."}
                ],
                "context": {
                    "user_inputs": {
                        "water_ph": 4.5,
                        "water_ec": 2.0,
                        "water_tds": 1.0,
                        "water_temperature": 21.0,
                        "air_temperature": 22.0,
                        "humidity": 60.0,
                        "co2": 350.0,
                        "nutrient_solution_ml": 400.0,
                        "water_consumption_l": 170.0,
                        "acid_consumption_ml": 40.0,
                        "initial_height_cm": 12.0,
                        "initial_weight_g": 4.0,
                        "initial_root_length_cm": 7.0,
                    },
                    "prediction_result": {
                        "prediction_value": 245.5,
                        "growth_category": "Poor"
                    },
                    "recommendation_outputs": [
                        {
                            "parameter": "Water pH",
                            "status": "Critical",
                            "action": "Immediately add pH-up solution."
                        }
                    ],
                    "explanation_output": {
                        "improvement_opportunities": [
                            {"factor": "Water pH", "explanation": "Water pH is critically low (4.5)."}
                        ]
                    }
                }
            }
        }
    }

def detect_intent(message: str, conversation_history: list) -> str:
    query = message.lower().strip()
    
    # Identify follow-up
    is_followup = False
    resolved_query = query
    ambiguous_keywords = ["it", "that", "this", "them", "fix", "solve", "why", "how", "adjust", "range", "value"]
    query_words = query.split()
    
    prev_user_query = None
    if conversation_history:
        for msg in reversed(conversation_history):
            if isinstance(msg, dict) and msg.get("role") == "user":
                prev_user_query = msg.get("content", "").lower().strip()
                break
            elif hasattr(msg, "role") and hasattr(msg, "content") and msg.role == "user":
                prev_user_query = msg.content.lower().strip()
                break
    
    if prev_user_query and (len(query_words) < 4 or any(w in ambiguous_keywords for w in query_words)):
        resolved_query = f"{prev_user_query} {query}"
        is_followup = True
        
    return IntentClassifier.classify_intent(message, resolved_query)

@router.post("/api/chat", summary="Chat with the HydroGrow AI Assistant")
@router.post("/chat", summary="Chat with the HydroGrow AI Assistant (alias)")
async def chat_assistant(
    data: ChatInput,
    current_user: Optional[Any] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Expose the conversational AI assistant to answer grow-room queries.
    Utilizes intent matching and a local RAG retriever to generate professional
    diagnostic answers based on prediction context and history.
    """
    try:
        context = data.context or {}
        conversation_history = data.conversation_history or []
        message = data.message
        
        db_conv_id = data.conversation_id
        if current_user:
            if db_conv_id:
                # Verify conversation ownership
                conv = crud.get_conversation(db, conversation_id=db_conv_id)
                if not conv or conv.user_id != current_user.id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to access this conversation thread"
                    )
                # Load message history
                db_messages = crud.get_messages_by_conversation_id(db, conversation_id=db_conv_id)
                conversation_history = [{"role": m.role, "content": m.content} for m in db_messages]
            else:
                # Auto-create new conversation thread
                title = message[:40] + ("..." if len(message) > 40 else "")
                conv = crud.create_conversation(db, user_id=current_user.id, title=title)
                db_conv_id = conv.id
        
        # Build context if they pass parameters directly inside the context dictionary
        if "user_inputs" not in context and any(k in context for k in ["water_ph", "air_temperature", "water_ec"]):
            # The inputs are direct, let's map them to 13-input format
            user_inputs = {
                "air_temperature": float(context.get("air_temperature", 22.0)),
                "humidity": float(context.get("humidity", 60.0)),
                "co2": float(context.get("co2", 450.0)),
                "water_ph": float(context.get("water_ph", 6.2)),
                "water_ec": float(context.get("water_ec", 2.0)),
                "water_tds": float(context.get("water_tds", context.get("water_ec", 2.0) * 0.5)),
                "water_temperature": float(context.get("water_temperature", 23.0)),
                "nutrient_solution_ml": float(context.get("nutrient_solution_ml", context.get("nutrient_solution", 400.0))),
                "water_consumption_l": float(context.get("water_consumption_l", context.get("water_consumption", 170.0))),
                "acid_consumption_ml": float(context.get("acid_consumption_ml", 40.0)),
                "initial_height_cm": float(context.get("initial_height_cm", context.get("seedling_height", 12.0))),
                "initial_weight_g": float(context.get("initial_weight_g", context.get("seedling_weight", 4.0))),
                "initial_root_length_cm": float(context.get("initial_root_length_cm", context.get("root_length", 7.0))),
            }
            try:
                pred_res = predict(user_inputs)
                recs = generate_recommendations(user_inputs)
                explanation = generate_explanation(user_inputs, pred_res, recs)
                context = {
                    "user_inputs": user_inputs,
                    "prediction_result": pred_res,
                    "recommendation_outputs": recs,
                    "explanation_output": explanation
                }
            except Exception:
                context = {
                    "user_inputs": user_inputs,
                    "prediction_result": {},
                    "recommendation_outputs": [],
                    "explanation_output": {}
                }
        
        # Inject conversation history into context as expected by ai_assistant
        context["conversation_history"] = conversation_history
        
        # Compile vision and farm contexts if authenticated
        if current_user:
            extra_context = compile_vision_and_farm_contexts(db, current_user.id)
            context.update(extra_context)
            
        # Get AI assistant response
        response = assistant.get_response(message, context)
        
        # Detect intent
        intent = detect_intent(message, conversation_history)
        
        # Retrieve sources using RAG retriever
        retrieved_chunks = retrieve(message, top_k=3, intent=intent)
        sources = list({chunk["source"] for chunk in retrieved_chunks if chunk.get("score", 0.0) > 0.08})
        
        # Save messages to database if user is authenticated
        if current_user and db_conv_id:
            crud.create_message(db, conversation_id=db_conv_id, role="user", content=message)
            crud.create_message(db, conversation_id=db_conv_id, role="assistant", content=response, sources=sources)
            # Update title & counts metadata
            ConversationManager.update_conversation_metadata(db, conversation_id=db_conv_id, new_message_content=message)
            
        return {
            "response": response,
            "sources": sources,
            "intent": intent,
            "conversation_id": db_conv_id
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "Assistant failed",
                "details": str(e)
            }
        )

@router.post("/api/chat/stream", summary="Stream response from HydroGrow AI Assistant")
@router.post("/chat/stream", summary="Stream response from HydroGrow AI Assistant (alias)")
async def chat_assistant_stream(
    data: ChatInput,
    current_user: Optional[Any] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Simulate streaming ChatGPT-style typing response from assistant.
    Yields event line chunks dynamically.
    """
    try:
        context = data.context or {}
        conversation_history = data.conversation_history or []
        message = data.message
        
        db_conv_id = data.conversation_id
        if current_user:
            if db_conv_id:
                # Verify conversation ownership
                conv = crud.get_conversation(db, conversation_id=db_conv_id)
                if not conv or conv.user_id != current_user.id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to access this conversation thread"
                    )
                # Load message history
                db_messages = crud.get_messages_by_conversation_id(db, conversation_id=db_conv_id)
                conversation_history = [{"role": m.role, "content": m.content} for m in db_messages]
            else:
                # Auto-create new conversation thread
                title = message[:40] + ("..." if len(message) > 40 else "")
                conv = crud.create_conversation(db, user_id=current_user.id, title=title)
                db_conv_id = conv.id

        # Build context if inputs passed directly
        if "user_inputs" not in context and any(k in context for k in ["water_ph", "air_temperature", "water_ec"]):
            user_inputs = {
                "air_temperature": float(context.get("air_temperature", 22.0)),
                "humidity": float(context.get("humidity", 60.0)),
                "co2": float(context.get("co2", 450.0)),
                "water_ph": float(context.get("water_ph", 6.2)),
                "water_ec": float(context.get("water_ec", 2.0)),
                "water_tds": float(context.get("water_tds", context.get("water_ec", 2.0) * 0.5)),
                "water_temperature": float(context.get("water_temperature", 23.0)),
                "nutrient_solution_ml": float(context.get("nutrient_solution_ml", context.get("nutrient_solution", 400.0))),
                "water_consumption_l": float(context.get("water_consumption_l", context.get("water_consumption", 170.0))),
                "acid_consumption_ml": float(context.get("acid_consumption_ml", 40.0)),
                "initial_height_cm": float(context.get("initial_height_cm", context.get("seedling_height", 12.0))),
                "initial_weight_g": float(context.get("initial_weight_g", context.get("seedling_weight", 4.0))),
                "initial_root_length_cm": float(context.get("initial_root_length_cm", context.get("root_length", 7.0))),
            }
            try:
                pred_res = predict(user_inputs)
                recs = generate_recommendations(user_inputs)
                explanation = generate_explanation(user_inputs, pred_res, recs)
                context = {
                    "user_inputs": user_inputs,
                    "prediction_result": pred_res,
                    "recommendation_outputs": recs,
                    "explanation_output": explanation
                }
            except Exception:
                context = {
                    "user_inputs": user_inputs,
                    "prediction_result": {},
                    "recommendation_outputs": [],
                    "explanation_output": {}
                }

        # Inject conversation history
        context["conversation_history"] = conversation_history
        
        # Compile vision and farm contexts if authenticated
        if current_user:
            extra_context = compile_vision_and_farm_contexts(db, current_user.id)
            context.update(extra_context)
            
        # Get response
        response = assistant.get_response(message, context)
        intent = detect_intent(message, conversation_history)
        retrieved_chunks = retrieve(message, top_k=3, intent=intent)
        sources = list({chunk["source"] for chunk in retrieved_chunks if chunk.get("score", 0.0) > 0.08})
        
        # Save messages to database if user is authenticated
        if current_user and db_conv_id:
            crud.create_message(db, conversation_id=db_conv_id, role="user", content=message)
            crud.create_message(db, conversation_id=db_conv_id, role="assistant", content=response, sources=sources)
            # Update title & counts metadata
            ConversationManager.update_conversation_metadata(db, conversation_id=db_conv_id, new_message_content=message)

        # Yield generator
        async def generator():
            # Split the text by tokens/words to stream
            words = re.split(r'(\s+)', response)
            for word in words:
                if not word:
                    continue
                chunk_data = {
                    "chunk": word,
                    "conversation_id": db_conv_id,
                    "sources": sources,
                    "intent": intent
                }
                yield json.dumps(chunk_data) + "\n"
                await asyncio.sleep(0.012) # simulated typing latency

        return StreamingResponse(generator(), media_type="text/event-stream")
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "Assistant stream failed",
                "details": str(e)
            }
        )

@router.get("/api/chat/context", summary="Get user profile and active crop context")
@router.get("/chat/context", summary="Get user profile and active crop context (alias)")
def get_chat_context(
    current_user: Optional[Any] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Expose user profile and latest crop prediction parameters.
    """
    profile = ContextBuilder.build_user_context(current_user.id if current_user else None, db)
    pred_context = ContextBuilder.build_prediction_context(current_user.id if current_user else None, db)

    return {
        "context": {
            "previous_prediction": f"{pred_context.get('predicted_weight', 'N/A')}g" if pred_context else "N/A",
            "crop": "lettuce",
            "profile_details": profile,
            "prediction_details": pred_context
        },
        "response": "Successfully retrieved grow-room context."
    }
