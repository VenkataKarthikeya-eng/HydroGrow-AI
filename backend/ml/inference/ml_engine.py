import time
from sqlalchemy.orm import Session
from backend.database.models import ModelPredictionLog, MLModel
from backend.ml.models.growth_model import GrowthModel
from backend.ml.models.disease_model import DiseaseModel

class MLEngine:
    """
    Production Inference Engine with Automatic Simulation Fallback.
    Logs latency, confidence scores, and prediction outputs.
    """

    _growth_model = None
    _disease_model = None

    @classmethod
    def get_growth_model(cls) -> GrowthModel:
        if cls._growth_model is None:
            cls._growth_model = GrowthModel()
        return cls._growth_model

    @classmethod
    def get_disease_model(cls) -> DiseaseModel:
        if cls._disease_model is None:
            cls._disease_model = DiseaseModel()
        return cls._disease_model

    @classmethod
    def run_growth_prediction(cls, db: Session, user_id: int, raw_inputs: dict) -> dict:
        t0 = time.time()
        model = cls.get_growth_model()
        pred_res = model.predict_growth(raw_inputs)
        inference_time_ms = round((time.time() - t0) * 1000.0, 2)

        pred_res["inference_time"] = f"{inference_time_ms}ms"

        # Log prediction to DB if active model exists
        try:
            active_model = db.query(MLModel).filter(
                MLModel.model_name == "GrowthPrediction",
                MLModel.status == "Active"
            ).first()

            log = ModelPredictionLog(
                user_id=user_id,
                model_id=active_model.id if active_model else None,
                input_data=raw_inputs,
                prediction_output=pred_res,
                confidence_score=pred_res.get("confidence_score", 90.0),
                inference_time=inference_time_ms
            )
            db.add(log)
            db.commit()
        except Exception:
            db.rollback()

        return pred_res

    @classmethod
    def run_disease_prediction(cls, db: Session, user_id: int, image_features: list = None, filename: str = "") -> dict:
        t0 = time.time()
        model = cls.get_disease_model()
        disease_res = model.predict_disease(image_features, filename=filename)
        inference_time_ms = round((time.time() - t0) * 1000.0, 2)

        disease_res["inference_time"] = f"{inference_time_ms}ms"

        try:
            active_model = db.query(MLModel).filter(
                MLModel.model_name == "DiseaseDetection",
                MLModel.status == "Active"
            ).first()

            log = ModelPredictionLog(
                user_id=user_id,
                model_id=active_model.id if active_model else None,
                input_data={"filename": filename},
                prediction_output=disease_res,
                confidence_score=disease_res.get("confidence_score", 95.0),
                inference_time=inference_time_ms
            )
            db.add(log)
            db.commit()
        except Exception:
            db.rollback()

        return disease_res
