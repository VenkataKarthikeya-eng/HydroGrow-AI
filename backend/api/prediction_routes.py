from typing import Optional, Any
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from backend.services.prediction.prediction import predict
from backend.services.intelligence.recommendation_engine import generate_recommendations
from backend.services.intelligence.explanation_engine import generate_explanation
from backend.database.connection import get_db
from backend.database import crud
from backend.authentication.jwt_handler import get_optional_current_user
from backend.ml.inference.ml_engine import MLEngine

router = APIRouter()

class PredictionInput(BaseModel):
    air_temperature: float = Field(..., description="Average greenhouse air temperature during growth cycle (°C)", ge=10.0, le=40.0)
    humidity: float = Field(..., description="Average relative humidity in the growing environment (%)", ge=30.0, le=90.0)
    co2: float = Field(..., description="Average CO2 concentration in the growing environment (ppm)", ge=300.0, le=1000.0)
    water_ph: float = Field(..., description="Average pH of the nutrient solution", ge=4.0, le=9.0)
    water_ec: float = Field(..., description="Average electrical conductivity of the nutrient solution (mS/cm)", ge=0.5, le=5.0)
    water_temperature: float = Field(..., description="Average temperature of the nutrient solution (°C)", ge=15.0, le=35.0)
    nutrient_solution: float = Field(..., description="Total nutrient solution added during growth cycle (mL)", ge=0.0, le=1500.0)
    water_consumption: float = Field(..., description="Total water consumed during growth cycle (L)", ge=0.0, le=500.0)
    seedling_height: float = Field(..., description="Average seedling height at transplant (cm)", ge=5.0, le=20.0)
    seedling_weight: float = Field(..., description="Average seedling weight at transplant (g)", ge=0.5, le=10.0)
    root_length: float = Field(..., description="Average root length of seedlings at transplant (cm)", ge=3.0, le=15.0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "air_temperature": 22.0,
                "humidity": 60.0,
                "co2": 450.0,
                "water_ph": 6.2,
                "water_ec": 2.0,
                "water_temperature": 23.0,
                "nutrient_solution": 400.0,
                "water_consumption": 170.0,
                "seedling_height": 12.0,
                "seedling_weight": 4.0,
                "root_length": 7.0,
            }
        }
    }

@router.post("/api/predict", summary="Predict Lettuce Growth and Get Recommendations")
async def predict_growth(
    data: PredictionInput,
    current_user: Optional[Any] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Predict lettuce growth fresh weight (g) and performance category,
    apply biological validations, generate cultivation recommendations,
    and generate explainable AI diagnostics from the parameters.
    """
    try:
        # Perform mapping and validation check
        water_tds = data.water_ec * 0.5
        acid_consumption_ml = 40.0
        
        user_inputs = {
            "air_temperature": data.air_temperature,
            "humidity": data.humidity,
            "co2": data.co2,
            "water_ph": data.water_ph,
            "water_ec": data.water_ec,
            "water_tds": water_tds,
            "water_temperature": data.water_temperature,
            "nutrient_solution_ml": data.nutrient_solution,
            "water_consumption_l": data.water_consumption,
            "acid_consumption_ml": acid_consumption_ml,
            "initial_height_cm": data.seedling_height,
            "initial_weight_g": data.seedling_weight,
            "initial_root_length_cm": data.root_length,
        }
        
        # 1. Run prediction
        pred_res = predict(user_inputs)
        
        # 1.1 Trigger ML Engine production inference log
        user_id_val = current_user.id if current_user else 1
        ml_res = MLEngine.run_growth_prediction(db, user_id_val, user_inputs)
        pred_res["confidence_score"] = ml_res.get("confidence_score", 93.5)
        pred_res["model_version"] = ml_res.get("model_version", "1.0.0")
        pred_res["inference_time"] = ml_res.get("inference_time", "3.2ms")
        
        # 2. Run recommendations
        recommendations = generate_recommendations(user_inputs)
        
        # 3. Run explanation
        explanation = generate_explanation(user_inputs, pred_res, recommendations)
        
        # Save prediction history to the database if the grower is authenticated
        if current_user:
            input_parameters = data.model_dump() if hasattr(data, "model_dump") else data.dict()
            predicted_weight = float(pred_res.get("predicted_weight", 0.0) or 0.0)
            growth_category = str(pred_res.get("growth_category", ""))
            
            crud.create_prediction(
                db=db,
                user_id=current_user.id,
                input_parameters=input_parameters,
                predicted_weight=predicted_weight,
                growth_category=growth_category,
                recommendations=recommendations,
                explanation=explanation
            )
            
        # Return response matching requirements
        return {
            "prediction": {
                "predicted_weight": pred_res.get("predicted_weight"),
                "growth_category": pred_res.get("growth_category")
            },
            "validation": {
                "prediction_value": pred_res.get("prediction_value"),
                "original_prediction": pred_res.get("original_prediction"),
                "was_adjusted": pred_res.get("was_adjusted"),
                "validation_message": pred_res.get("validation_message")
            },
            "recommendations": recommendations,
            "explanation": explanation,
            "metadata": {
                "derived_inputs": {
                    "water_tds": water_tds,
                    "acid_consumption_ml": acid_consumption_ml
                }
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "Prediction failed",
                "details": str(e)
            }
        )
