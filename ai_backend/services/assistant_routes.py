import re
import json
import asyncio
from typing import Optional, Any, List, Dict
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

router = APIRouter(tags=["AI Assistant"])

class ChatInput(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, Any]]] = None
    context: Optional[Dict[str, Any]] = None
    conversation_id: Optional[Any] = None

def get_assistant_response(user_query: str) -> tuple[str, List[str]]:
    query = user_query.lower().strip()
    
    # Out-of-domain question filter
    out_of_domain_keywords = ["car", "vehicle", "movie", "game", "president", "sports", "football", "crypto", "bitcoin"]
    if any(word in query.split() for word in out_of_domain_keywords):
        return (
            "I am specialized in hydroponics and crop management. "
            "Please ask questions related to farming, nutrients, or plant health.",
            []
        )

    # Hydroponics Domain Responses
    if "ec" in query or "nutrient" in query or "electrical conductivity" in query:
        response = (
            "### 🧪 Hydroponic Nutrient & EC Guidance\n\n"
            "For hydroponic lettuce during the **vegetative growth stage**, maintain water EC at **1.8 – 2.2 mS/cm**.\n\n"
            "- **Nursery Phase:** `1.2 – 1.6 mS/cm`\n"
            "- **Vegetative Phase:** `1.8 – 2.2 mS/cm`\n"
            "- **Mature / Pre-Harvest:** `2.0 – 2.4 mS/cm`\n\n"
            "**Key Advice:** Ensure continuous solution recirculation and keep water temperature under 22°C to prevent tip-burn."
        )
        sources = ["Hydroponics Crop Science Guide v2.4", "Section 4: Bioavailability & EC Range"]
    elif "ph" in query or "acid" in query:
        response = (
            "### 🧪 Water pH Optimization\n\n"
            "Target a water pH between **5.8 and 6.2** for hydroponic lettuce.\n\n"
            "- If pH rises above **6.5**, micronutrients like iron and manganese become insoluble, causing interveinal chlorosis.\n"
            "- If pH drops below **5.2**, root tissue injury can occur.\n\n"
            "**Action:** Calibrate pH probes daily and dose pH-down (phosphoric acid) as needed."
        )
        sources = ["Hydroponics Crop Science Guide v2.4", "Section 3: pH Control Protocols"]
    elif "root" in query or "rot" in query or "pythium" in query:
        response = (
            "### 🌱 Pathology Management: Root Rot (Pythium)\n\n"
            "Root rot (*Pythium*) is triggered by low dissolved oxygen and water temperatures exceeding **24°C**.\n\n"
            "- **Prevention:** Maintain root zone water temperature below **22°C**.\n"
            "- **Aeration:** Ensure dissolved oxygen (DO) levels stay above **6.5 mg/L**.\n"
            "- **Treatment:** Flush reservoir and apply beneficial microbes (*Bacillus amyloliquefaciens*)."
        )
        sources = ["Pathology Index for Closed Loop Systems", "Page 42: Pythium Management"]
    elif "growth" in query or "stage" in query or "yield" in query or "predict" in query:
        response = (
            "### 📈 Lettuce Growth Stage Pipeline\n\n"
            "Hydroponic butterhead lettuce typically matures in **28 days** across 4 growth phases:\n\n"
            "1. **Germination (Days 1–3):** Dark, high humidity\n"
            "2. **Nursery Stage (Days 4–10):** DLI 12–14 mol/m²/day\n"
            "3. **Vegetative Phase (Days 11–20):** Rapid leaf expansion, EC 1.8–2.2 mS/cm\n"
            "4. **Harvest Stage (Days 21–28):** Final head formation, weight 180–350g\n"
        )
        sources = ["Crop Lifecycle Manual v1.2", "Page 15: Growth Stages"]
    else:
        response = (
            "Based on our hydroponics crop science index, maintaining an EC level between 1.8 and 2.4 mS/cm "
            "and water pH between 5.8 and 6.4 ensures optimal nutrient bioavailability for leafy greens like lettuce and basil."
        )
        sources = ["Hydroponics Crop Science Guide v2.4"]

    return response, sources

@router.post("/api/chat", summary="Chat with the HydroGrow AI Assistant")
@router.post("/chat", summary="Chat with the HydroGrow AI Assistant (alias)")
async def chat_assistant(data: ChatInput):
    """
    Standalone Assistant Endpoint for lightweight AI backend deployments.
    """
    try:
        message = data.message or ""
        response, sources = get_assistant_response(message)
        return {
            "response": response,
            "sources": sources,
            "intent": "general_inquiry",
            "conversation_id": data.conversation_id
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": True, "message": "Assistant failed", "details": str(e)}
        )

@router.post("/api/chat/stream", summary="Stream response from HydroGrow AI Assistant")
@router.post("/chat/stream", summary="Stream response from HydroGrow AI Assistant (alias)")
async def chat_assistant_stream(data: ChatInput):
    """
    Simulated streaming typing response for lightweight AI backend deployments.
    """
    try:
        message = data.message or ""
        response, sources = get_assistant_response(message)

        async def generator():
            words = re.split(r'(\s+)', response)
            for word in words:
                if not word:
                    continue
                chunk_data = {
                    "chunk": word,
                    "conversation_id": data.conversation_id,
                    "sources": sources,
                    "intent": "general_inquiry"
                }
                yield json.dumps(chunk_data) + "\n"
                await asyncio.sleep(0.01)

        return StreamingResponse(generator(), media_type="text/event-stream")
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": True, "message": "Assistant stream failed", "details": str(e)}
        )

@router.get("/api/chat/context", summary="Get user profile and active crop context")
@router.get("/chat/context", summary="Get user profile and active crop context (alias)")
def get_chat_context():
    return {
        "context": {
            "previous_prediction": "320g",
            "crop": "lettuce",
            "profile_details": {"username": "Grower", "role": "Head Grower"},
            "prediction_details": {}
        },
        "response": "Successfully retrieved grow-room context."
    }
