import os
import sys
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure ai_backend directory is on path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.growth_prediction_service import growth_service
from services.nutrient_prediction_service import nutrient_service
from services.crop_validation_service import crop_validation_service

app = FastAPI(
    title="HydroGrow AI Plant Doctor Backend",
    description="Lightweight production API for HydroGrow AI Plant Doctor",
    version="1.0.0"
)

# Allowed origins for production & development
origins = [
    "*",
    "http://localhost:5173",
    "http://localhost:3000",
    "https://hydrogrow-ai.vercel.app",
    "https://hydrogrow.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", summary="Health check endpoint")
def health_check():
    return {
        "status": "healthy",
        "service": "HydroGrow AI Plant Doctor Backend"
    }


@app.post("/api/vision/predict-growth", summary="Predict Lettuce Growth Stage and Growth Day from Plant Image")
async def predict_growth_stage(
    file: UploadFile = File(...)
):
    """
    Accepts plant image upload and returns lettuce growth stage, predicted growth day,
    model confidence score, and stage-specific cultivation recommendations.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a valid filename.")
    
    contents = await file.read()
    
    # Crop Identity Validation Security Gate
    val_check = crop_validation_service.validate_crop_image(contents)
    if val_check.get("status") == "rejected":
        return JSONResponse(
            status_code=400,
            content=val_check
        )

    try:
        result = growth_service.predict_image(contents)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing failed: {str(e)}")


@app.post("/api/vision/predict-nutrient", summary="Detect Lettuce Nutrient Deficiency from Leaf Image")
async def predict_nutrient_condition(
    file: UploadFile = File(...)
):
    """
    Accepts plant leaf image upload and returns nutrient condition (Healthy, Nitrogen Deficiency,
    Phosphorus Deficiency, Potassium Deficiency), confidence score, and tailored recommendation.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a valid filename.")

    contents = await file.read()
    
    # Crop Identity Validation Security Gate
    val_check = crop_validation_service.validate_crop_image(contents)
    if val_check.get("status") == "rejected":
        return JSONResponse(
            status_code=400,
            content=val_check
        )

    try:
        result = nutrient_service.predict_image(contents)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Nutrient analysis failed: {str(e)}")


@app.post("/api/vision/plant-analysis", summary="Combined Growth & Nutrient Plant Analysis Scanner")
async def analyze_plant_combined(
    file: UploadFile = File(...)
):
    """
    Combines Growth Stage & Day Prediction and Nutrient Deficiency Detection
    into a unified diagnostic response with overall cultivation recommendations.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a valid filename.")

    contents = await file.read()

    # Crop Identity Validation Security Gate
    val_check = crop_validation_service.validate_crop_image(contents)
    if val_check.get("status") == "rejected":
        return JSONResponse(
            status_code=400,
            content=val_check
        )

    try:
        growth_res = growth_service.predict_image(contents)
        nutrient_res = nutrient_service.predict_image(contents)

        if nutrient_res.get("condition") == "Healthy":
            overall_rec = f"Plant growth is in {growth_res.get('growth_stage')} stage (Day {growth_res.get('growth_day')}). {nutrient_res.get('recommendation')}"
        else:
            overall_rec = f"Action required: Detected {nutrient_res.get('condition')} at Day {growth_res.get('growth_day')}. {nutrient_res.get('recommendation')}"

        return {
            "growth_prediction": {
                "stage": growth_res.get("growth_stage"),
                "growth_day": growth_res.get("growth_day"),
                "confidence": growth_res.get("confidence")
            },
            "nutrient_prediction": {
                "condition": nutrient_res.get("condition"),
                "confidence": nutrient_res.get("confidence")
            },
            "recommendation": overall_rec
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Combined plant analysis failed: {str(e)}")
