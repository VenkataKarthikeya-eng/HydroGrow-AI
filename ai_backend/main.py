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

    t_pipeline_start = time.perf_counter()

    # Step 1: Single-pass Image Decode
    t_decode_start = time.perf_counter()
    try:
        image = Image.open(io.BytesIO(contents)).convert('RGB')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")
    t_decode = time.perf_counter() - t_decode_start

    # Step 2: Single-pass Preprocessing
    t_prep_start = time.perf_counter()
    img_resized = image.resize((224, 224))
    arr_224 = np.array(img_resized, dtype=np.float32) / 255.0
    batch_arr = np.expand_dims(arr_224, axis=0)
    t_prep = time.perf_counter() - t_prep_start

    # Step 3: Crop Identity Validation Security Gate
    print("\n[Pipeline]")
    print("Crop Validation Started")
    t_crop_start = time.perf_counter()
    val_check = crop_validation_service.validate_crop_image(image_input=image, arr_input=batch_arr)
    t_crop = time.perf_counter() - t_crop_start
    print("Crop Validation Completed")

    if val_check.get("status") == "rejected":
        return JSONResponse(
            status_code=400,
            content=val_check
        )

    try:
        # Step 4: Parallel Inference for Growth and Nutrient Models
        print("\nStarting parallel inference:")
        print("Growth Prediction Started")
        print("Nutrient Prediction Started")

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            f_growth = executor.submit(growth_service.predict_image_fast, image, batch_arr)
            f_nutrient = executor.submit(nutrient_service.predict_image_fast, image, batch_arr)

            growth_res, t_growth = f_growth.result()
            nutrient_res, t_nutrient = f_nutrient.result()

        print(f"Growth Completed: {t_growth:.3f}s")
        print(f"Nutrient Completed: {t_nutrient:.3f}s")

        # Step 5: Recommendation Generation
        t_rec_start = time.perf_counter()
        if nutrient_res.get("condition") == "Healthy":
            overall_rec = f"Plant growth is in {growth_res.get('growth_stage')} stage (Day {growth_res.get('growth_day')}). {nutrient_res.get('recommendation')}"
        else:
            overall_rec = f"Action required: Detected {nutrient_res.get('condition')} at Day {growth_res.get('growth_day')}. {nutrient_res.get('recommendation')}"
        t_rec = time.perf_counter() - t_rec_start

        t_total = time.perf_counter() - t_pipeline_start
        print("Combined Result Generated\n")

        print(
            f"[Performance Debug]\n"
            f"Image Decode: {t_decode:.3f}s\n"
            f"Preprocessing: {t_prep:.3f}s\n"
            f"Crop Validation: {t_crop:.3f}s\n"
            f"Growth Prediction: {t_growth:.3f}s\n"
            f"Nutrient Prediction: {t_nutrient:.3f}s\n"
            f"Recommendation Generation: {t_rec:.3f}s\n"
            f"Total Time: {t_total:.3f}s\n"
        )

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

