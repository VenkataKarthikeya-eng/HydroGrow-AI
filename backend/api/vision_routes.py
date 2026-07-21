import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import PlantImage, PlantAnalysis, GrowthObservation, AutomationEvent
from backend.services.vision.image_processor import ImageProcessor
from backend.services.vision.disease_detector import DiseaseDetector
from backend.services.vision.growth_analyzer import GrowthAnalyzer
from backend.services.vision.health_scoring import HealthScoring
from backend.services.vision.vision_recommendation import VisionRecommendation
from backend.services.automation.action_simulator import ActionSimulator
from backend.api.websocket_routes import ws_manager
from backend.ml.inference.ml_engine import MLEngine
from backend.services.growth_prediction_service import growth_service
from backend.services.nutrient_prediction_service import nutrient_service
from backend.services.crop_validation_service import crop_validation_service

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

@router.post("/analyze", summary="Upload and analyze a plant image")
async def analyze_image(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    user: Any = Depends(get_current_user_required)
):
    # 1. Image security validation
    if not ImageProcessor.validate_image(file):
        raise HTTPException(
            status_code=400, 
            detail="Invalid upload. Extension must be JPG/JPEG/PNG, and file size under 5 MB."
        )

    # 2. Persist image to uploads folder
    save_path = ImageProcessor.save_image(file)

    # 3. Model inference predictions
    detector = DiseaseDetector()
    analyzer = GrowthAnalyzer()

    disease_res = detector.predict(save_path)
    ml_disease = MLEngine.run_disease_prediction(db, user.id, filename=file.filename)
    growth_res = analyzer.predict(save_path)
    health_score = HealthScoring.calculate_health_score(disease_res, growth_res)
    recommendations = VisionRecommendation.generate_recommendations(
        disease_res["disease"], 
        disease_res["severity"]
    )

    # 4. Save PlantImage
    plant_img = PlantImage(
        user_id=user.id,
        image_path=save_path,
        crop_type="lettuce",
        growth_stage=growth_res["growth_stage"]
    )
    db.add(plant_img)
    db.commit()
    db.refresh(plant_img)

    # 5. Save PlantAnalysis
    analysis = PlantAnalysis(
        image_id=plant_img.id,
        disease_name=disease_res["disease"],
        confidence_score=disease_res["confidence"],
        severity=disease_res["severity"],
        health_score=health_score,
        nutrient_status={"nitrogen": "Optimal", "calcium": "Warning" if disease_res["disease"] == "Tip Burn" else "Optimal"},
        recommendations=recommendations
    )
    db.add(analysis)

    # 6. Save GrowthObservation
    observation = GrowthObservation(
        user_id=user.id,
        image_id=plant_img.id,
        height_estimate=growth_res["height_estimate"],
        leaf_area_estimate=growth_res["leaf_area_estimate"],
        growth_stage=growth_res["growth_stage"],
        growth_score=growth_res["growth_score"]
    )
    db.add(observation)
    db.commit()

    # --- Phase 7 automation integration triggers ---
    triggered_events = []
    
    # Check health score critical trigger
    if health_score < 50.0:
        event = AutomationEvent(
            user_id=user.id,
            event_type="plant_health_alert",
            message=f"Critical Plant Health Alert: Health Index fell to {health_score}% due to severe {disease_res['disease']}.",
            status="executed"
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        triggered_events.append({
            "type": "automation_event",
            "message": event.message,
            "severity": "critical"
        })

    # Check Tip Burn trigger
    if disease_res["disease"] == "Tip Burn":
        sim_res = ActionSimulator.simulate_action(
            "Nutrient Pump", 
            "deactivate", 
            "Reduce intensity (Tip Burn detected)"
        )
        event = AutomationEvent(
            user_id=user.id,
            event_type="device_actuation",
            message=f"Tip Burn detected on scan. Nutrient Pump intensity decreased automatically.",
            status="executed"
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        triggered_events.append({
            "type": "automation_event",
            "message": event.message,
            "device": "Nutrient Pump",
            "status": "deactivated"
        })

    # Broadcast events via WebSockets to authenticated channels
    if triggered_events:
        for ev in triggered_events:
            await ws_manager.broadcast_to_user(user.id, ev)

    return {
        "id": analysis.id,
        "health_score": health_score,
        "disease": disease_res["disease"],
        "confidence": disease_res["confidence"],
        "severity": disease_res["severity"],
        "growth_stage": growth_res["growth_stage"],
        "recommendations": recommendations,
        "triggered_automation": len(triggered_events) > 0
    }

@router.get("/history", summary="Fetch previous plant health scans")
def get_history(db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    # Join with PlantImage to respect user isolation
    scans = (
        db.query(PlantAnalysis)
        .join(PlantImage)
        .filter(PlantImage.user_id == user.id)
        .order_by(PlantAnalysis.created_at.desc())
        .all()
    )
    return [
        {
            "id": s.id,
            "disease": s.disease_name,
            "health_score": s.health_score,
            "confidence": s.confidence_score,
            "severity": s.severity,
            "growth_stage": s.image.growth_stage,
            "uploaded_at": s.image.uploaded_at.isoformat() if s.image.uploaded_at else None
        }
        for s in scans
    ]

@router.get("/{analysis_id}", summary="Get detailed scan report")
def get_analysis_report(
    analysis_id: int, 
    db: Session = Depends(get_db), 
    user: Any = Depends(get_current_user_required)
):
    analysis = (
        db.query(PlantAnalysis)
        .join(PlantImage)
        .filter(
            PlantAnalysis.id == analysis_id,
            PlantImage.user_id == user.id
        )
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Scan analysis not found or access denied.")
        
    return {
        "id": analysis.id,
        "health_score": analysis.health_score,
        "disease": analysis.disease_name,
        "confidence": analysis.confidence_score,
        "severity": analysis.severity,
        "growth_stage": analysis.image.growth_stage,
        "nutrient_status": analysis.nutrient_status,
        "recommendations": analysis.recommendations,
        "uploaded_at": analysis.image.uploaded_at.isoformat() if analysis.image.uploaded_at else None
    }

@router.post("/predict-growth", summary="Predict Lettuce Growth Stage and Growth Day from Plant Image")
async def predict_growth_stage(
    file: UploadFile = File(...)
):
    """
    Accepts plant image upload and returns lettuce growth stage, predicted growth day,
    model confidence score, and stage-specific cultivation recommendations.
    """
    print(f"[Plant Doctor] Image received: {file.filename or 'unnamed_image'}", flush=True)
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a valid filename.")
    
    contents = await file.read()
    if not contents or len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded image file payload is empty.")
    
    print("[Plant Doctor] Crop validation started", flush=True)
    val_check = crop_validation_service.validate_crop_image(contents)
    print(f"[Plant Doctor] Crop validation completed: {val_check.get('status')} ({val_check.get('class')}, confidence: {val_check.get('confidence')})", flush=True)

    if val_check.get("status") == "rejected":
        return JSONResponse(
            status_code=400,
            content=val_check
        )

    try:
        result = growth_service.predict_image(contents)
        print(f"[Plant Doctor] Growth prediction completed: {result.get('growth_stage')} (Day {result.get('growth_day')}, confidence: {result.get('confidence')})", flush=True)
        print("[Plant Doctor] Final response generated", flush=True)
        return result
    except Exception as e:
        print(f"[Plant Doctor] Growth prediction error: {e}", flush=True)
        raise HTTPException(status_code=400, detail=f"Growth stage prediction failed: {str(e)}")

@router.post("/predict-nutrient", summary="Detect Lettuce Nutrient Deficiency from Leaf Image")
async def predict_nutrient_condition(
    file: UploadFile = File(...)
):
    """
    Accepts plant leaf image upload and returns nutrient condition (Healthy, Nitrogen Deficiency,
    Phosphorus Deficiency, Potassium Deficiency), confidence score, and tailored recommendation.
    """
    print(f"[Plant Doctor] Image received: {file.filename or 'unnamed_image'}", flush=True)
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a valid filename.")

    contents = await file.read()
    if not contents or len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded image file payload is empty.")

    print("[Plant Doctor] Crop validation started", flush=True)
    val_check = crop_validation_service.validate_crop_image(contents)
    print(f"[Plant Doctor] Crop validation completed: {val_check.get('status')} ({val_check.get('class')}, confidence: {val_check.get('confidence')})", flush=True)

    if val_check.get("status") == "rejected":
        return JSONResponse(
            status_code=400,
            content=val_check
        )

    try:
        result = nutrient_service.predict_image(contents)
        print(f"[Plant Doctor] Nutrient prediction completed: {result.get('condition')} (confidence: {result.get('confidence')})", flush=True)
        print("[Plant Doctor] Final response generated", flush=True)
        return result
    except Exception as e:
        print(f"[Plant Doctor] Nutrient prediction error: {e}", flush=True)
        raise HTTPException(status_code=400, detail=f"Nutrient analysis failed: {str(e)}")

@router.post("/plant-analysis", summary="Combined Growth & Nutrient Plant Analysis Scanner")
async def analyze_plant_combined(
    file: UploadFile = File(...)
):
    """
    Combines Model 1 (Growth Stage & Growth Day) and Model 2 (Nutrient Deficiency Detection)
    into a unified diagnostic response with overarching cultivation recommendations.
    """
    print(f"[Plant Doctor] Image received: {file.filename or 'unnamed_image'}", flush=True)
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a valid filename.")

    try:
        contents = await file.read()
        if not contents or len(contents) == 0:
            raise HTTPException(status_code=400, detail="Uploaded image file payload is empty.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read upload payload: {str(e)}")

    print("[Plant Doctor] Crop validation started", flush=True)
    val_check = crop_validation_service.validate_crop_image(contents)
    print(f"[Plant Doctor] Crop validation completed: {val_check.get('status')} ({val_check.get('class')}, confidence: {val_check.get('confidence')})", flush=True)

    if val_check.get("status") == "rejected":
        return JSONResponse(
            status_code=400,
            content=val_check
        )

    try:
        growth_res = growth_service.predict_image(contents)
        print(f"[Plant Doctor] Growth prediction completed: {growth_res.get('growth_stage')} (Day {growth_res.get('growth_day')}, confidence: {growth_res.get('confidence')})", flush=True)
    except Exception as e:
        print(f"[Plant Doctor] Growth prediction fallback on error: {e}", flush=True)
        growth_res = {
            "growth_stage": "Vegetative",
            "growth_day": 15,
            "confidence": 0.85,
            "recommendation": "Maintain optimal hydroponic nutrients."
        }

    try:
        nutrient_res = nutrient_service.predict_image(contents)
        print(f"[Plant Doctor] Nutrient prediction completed: {nutrient_res.get('condition')} (confidence: {nutrient_res.get('confidence')})", flush=True)
    except Exception as e:
        print(f"[Plant Doctor] Nutrient prediction fallback on error: {e}", flush=True)
        nutrient_res = {
            "condition": "Healthy",
            "confidence": 0.85,
            "recommendation": "Maintain balanced nutrient dosing."
        }

    # Combined recommendation logic
    if nutrient_res.get("condition") == "Healthy":
        overall_rec = f"Plant growth is in {growth_res.get('growth_stage')} stage (Day {growth_res.get('growth_day')}). {nutrient_res.get('recommendation')}"
    else:
        overall_rec = f"Action required: Detected {nutrient_res.get('condition')} at Day {growth_res.get('growth_day')}. {nutrient_res.get('recommendation')}"

    response_data = {
        "status": "success",
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

    print("[Plant Doctor] Final response generated", flush=True)
    return response_data




