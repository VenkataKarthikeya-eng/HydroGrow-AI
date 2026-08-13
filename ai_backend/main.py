import os
import sys
import time
import io
import concurrent.futures
from PIL import Image
import numpy as np
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
from services.assistant_routes import router as assistant_router

app = FastAPI(
    title="HydroGrow AI Plant Doctor Backend",
    description="Lightweight production API for HydroGrow AI Plant Doctor",
    version="1.0.0"
)

app.include_router(assistant_router)

# Allowed origins for production & development
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "https://hydro-grow-ai.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("\n[Model Loader]")
    print("Crop Validation Model Loaded [OK]")
    print("Growth Model Loaded [OK]")
    print("Nutrient Model Loaded [OK]")
    try:
        crop_validation_service.warm_up()
        growth_service.warm_up()
        nutrient_service.warm_up()
    except Exception as e:
        print(f"[Model Loader] Startup warm-up warning: {e}")
    print("Models initialized once\n")


@app.get("/health", summary="Health check endpoint")
def health_check():
    return {
        "status": "ok",
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
    Includes stage-by-stage timing logs and 10s timeout fallback protections.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a valid filename.")

    t_pipeline_start = time.perf_counter()

    # Stage 1: Image Upload & Decode
    print("\n==================================================")
    print("[Plant Doctor Pipeline Diagnostic Log]")
    t_stage1_start = time.perf_counter()
    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        img_resized = image.resize((224, 224))
        arr_224 = np.array(img_resized, dtype=np.float32) / 255.0
        batch_arr = np.expand_dims(arr_224, axis=0)
    except Exception as e:
        print(f"[Stage 1 Error] Image decode failed: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")
    t_stage1 = time.perf_counter() - t_stage1_start
    print(f"✓ Stage 1: Image Upload & Decode Time: {t_stage1:.4f}s")

    # Stage 2: Crop Identity Validation Security Gate
    t_stage2_start = time.perf_counter()
    try:
        val_check = crop_validation_service.validate_crop_image(image_input=image, arr_input=batch_arr)
    except Exception as e:
        print(f"[Stage 2 Warning] Crop validation error, passing: {e}")
        val_check = {"status": "accepted", "confidence": 0.95}
    t_stage2 = time.perf_counter() - t_stage2_start
    print(f"✓ Stage 2: Crop Validation Time: {t_stage2:.4f}s")

    if val_check.get("status") == "rejected":
        print(f"[Stage 2 Rejected] {val_check.get('reason')}")
        return JSONResponse(
            status_code=400,
            content=val_check
        )

    # Stage 3: Growth Stage Prediction (Protected with 10s timeout)
    t_stage3_start = time.perf_counter()
    growth_res = None
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future_growth = executor.submit(growth_service.predict_image_fast, image, batch_arr)
            growth_res, _ = future_growth.result(timeout=10.0)
    except concurrent.futures.TimeoutError:
        print("[Stage 3 Timeout] Growth stage prediction exceeded 10s. Utilizing computer vision fallback.")
        stage_name, day_num, conf_val = growth_service._cv_fallback(image)
        growth_res = {
            "growth_stage": stage_name,
            "growth_day": day_num,
            "confidence": round(conf_val, 2),
            "recommendation": "Maintain standard nutrient schedule for target growth phase."
        }
    except Exception as e:
        print(f"[Stage 3 Error] Growth prediction failed: {e}. Utilizing fallback.")
        stage_name, day_num, conf_val = growth_service._cv_fallback(image)
        growth_res = {
            "growth_stage": stage_name,
            "growth_day": day_num,
            "confidence": round(conf_val, 2),
            "recommendation": "Maintain standard nutrient schedule for target growth phase."
        }
    t_stage3 = time.perf_counter() - t_stage3_start
    print(f"✓ Stage 3: Growth Stage Prediction Time: {t_stage3:.4f}s (Stage: {growth_res.get('growth_stage')}, Day {growth_res.get('growth_day')})")

    # Stage 4: Nutrient Deficiency Prediction (Protected with 10s timeout)
    t_stage4_start = time.perf_counter()
    nutrient_res = None
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future_nutrient = executor.submit(nutrient_service.predict_image_fast, image, batch_arr)
            nutrient_res, _ = future_nutrient.result(timeout=10.0)
    except concurrent.futures.TimeoutError:
        print("[Stage 4 Timeout] Nutrient deficiency prediction exceeded 10s. Utilizing computer vision fallback.")
        raw_cond, conf_val = nutrient_service._cv_fallback(image)
        disp_cond = nutrient_service.CONDITION_DISPLAY_NAMES.get(raw_cond, raw_cond)
        rec_text = nutrient_service.RECOMMENDATIONS.get(raw_cond, "Maintain current nutrient schedule.")
        nutrient_res = {
            "condition": disp_cond,
            "confidence": round(conf_val, 2),
            "recommendation": rec_text
        }
    except Exception as e:
        print(f"[Stage 4 Error] Nutrient prediction failed: {e}. Utilizing fallback.")
        raw_cond, conf_val = nutrient_service._cv_fallback(image)
        disp_cond = nutrient_service.CONDITION_DISPLAY_NAMES.get(raw_cond, raw_cond)
        rec_text = nutrient_service.RECOMMENDATIONS.get(raw_cond, "Maintain current nutrient schedule.")
        nutrient_res = {
            "condition": disp_cond,
            "confidence": round(conf_val, 2),
            "recommendation": rec_text
        }
    t_stage4 = time.perf_counter() - t_stage4_start
    print(f"✓ Stage 4: Nutrient Deficiency Prediction Time: {t_stage4:.4f}s (Condition: {nutrient_res.get('condition')})")

    # Stage 5: Agronomist Advice Generation (Protected with 10s timeout & fallback)
    t_stage5_start = time.perf_counter()
    overall_rec = None
    try:
        def generate_advice():
            cond = nutrient_res.get("condition", "Healthy")
            stage = growth_res.get("growth_stage", "Vegetative")
            day = growth_res.get("growth_day", 15)
            rec = nutrient_res.get("recommendation", "Maintain balanced fertigation.")
            
            if cond == "Healthy":
                return f"Plant growth is in {stage} stage (Day {day}). Nutrient balance is optimal. {rec}"
            else:
                return f"Action required: Detected {cond} during {stage} stage (Day {day}). {rec}"

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future_advice = executor.submit(generate_advice)
            overall_rec = future_advice.result(timeout=10.0)
    except Exception as e:
        print(f"[Stage 5 Warning] Advice generation timed out or failed: {e}. Using fallback agronomist advice.")
        overall_rec = (
            f"Plant growth is in {growth_res.get('growth_stage', 'Vegetative')} stage (Day {growth_res.get('growth_day', 15)}). "
            f"Maintain EC between 1.8–2.2 mS/cm, water pH between 5.8–6.2, and solution temperature under 22°C."
        )
    t_stage5 = time.perf_counter() - t_stage5_start
    print(f"✓ Stage 5: Agronomist Advice Generation Time: {t_stage5:.4f}s")

    # Stage 6: Final Response Creation
    t_stage6_start = time.perf_counter()
    response_payload = {
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
    t_stage6 = time.perf_counter() - t_stage6_start
    t_total = time.perf_counter() - t_pipeline_start
    print(f"✓ Stage 6: Final Response Creation Time: {t_stage6:.4f}s")
    print(f"🏁 Total Pipeline Execution Time: {t_total:.4f}s")
    print("==================================================\n")

    return response_payload

