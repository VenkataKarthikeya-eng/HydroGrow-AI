import os
import datetime
from sqlalchemy.orm import Session
from backend.database.models import MLModel, TrainingDataset
from backend.ml.preprocessing.data_processor import DataProcessor
from backend.ml.models.growth_model import GrowthModel
from backend.ml.evaluation.model_metrics import ModelMetrics

class TrainPipeline:
    """
    Automated Background Training Pipeline & Model Registry Manager.
    """

    @staticmethod
    def run_growth_model_training(db: Session, version_name: str = None) -> dict:
        # 1. Generate / load training dataset
        X, y = DataProcessor.generate_synthetic_agronomic_dataset(num_samples=600)

        # 2. Train Growth Model
        model_instance = GrowthModel()
        r2_score = model_instance.train_growth_model(X, y)

        # Evaluate predictions
        y_pred = model_instance.model.predict(X)
        metrics = ModelMetrics.evaluate_regression(y, y_pred)

        # 3. Determine version name
        if not version_name:
            version_name = f"v1.{int(datetime.datetime.utcnow().timestamp()) % 1000}"

        # 4. Archive existing Active models of type GrowthPrediction
        db.query(MLModel).filter(
            MLModel.model_name == "GrowthPrediction",
            MLModel.status == "Active"
        ).update({"status": "Archived"})

        # 5. Register new MLModel entry in DB
        new_model = MLModel(
            model_name="GrowthPrediction",
            model_type="Regression",
            version=version_name,
            algorithm="RandomForestRegressor",
            accuracy_score=metrics["r2_score"],
            training_dataset="HydroGrow Lettuce Agronomic Dataset v1",
            model_path=model_instance.model_path,
            status="Active"
        )
        db.add(new_model)

        # Register TrainingDataset if absent
        ds_exists = db.query(TrainingDataset).filter(TrainingDataset.dataset_name == "HydroGrow Lettuce Agronomic Dataset v1").first()
        if not ds_exists:
            new_ds = TrainingDataset(
                dataset_name="HydroGrow Lettuce Agronomic Dataset v1",
                dataset_type="Agronomic Predictors",
                source="Greenhouse Sensors & Lab Calibrations",
                sample_count=600,
                features=["air_temperature", "humidity", "co2", "water_ph", "water_ec", "water_temperature", "nutrient_solution", "water_consumption", "seedling_height", "seedling_weight", "root_length"],
                description="Synthesized agronomic predictor vectors for lettuce biomass expansion."
            )
            db.add(new_ds)

        db.commit()
        db.refresh(new_model)

        return {
            "model_id": new_model.id,
            "version": version_name,
            "algorithm": new_model.algorithm,
            "metrics": metrics,
            "status": "Active"
        }
