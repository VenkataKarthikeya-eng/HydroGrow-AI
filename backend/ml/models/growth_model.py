import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from backend.ml.preprocessing.data_processor import DataProcessor, FEATURE_ORDER

MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "saved", "growth_model.joblib")

class GrowthModel:
    """
    Lettuce Biomass & Harvest Yield Scikit-Learn Regressor.
    """

    def __init__(self, model_path: str = MODEL_SAVE_PATH):
        self.model_path = model_path
        self.version = "1.0.0"
        self.algorithm = "RandomForestRegressor"
        self.model = None
        self._load_saved_model()

    def _load_saved_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception:
                self.model = None

    def train_growth_model(self, X_train: np.ndarray, y_train: np.ndarray) -> float:
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)
        self.model.fit(X_train, y_train)
        joblib.dump(self.model, self.model_path)
        
        # Calculate R2 score on training set
        score = float(self.model.score(X_train, y_train))
        return round(score, 4)

    def predict_growth(self, features_dict: dict) -> dict:
        if self.model is None:
            # Fallback to simulation heuristic algorithm
            return self._fallback_prediction(features_dict)

        try:
            vector = DataProcessor.normalize_features(features_dict)
            X = np.array([vector])
            predicted_weight = float(self.model.predict(X)[0])
            predicted_weight = round(max(100.0, min(500.0, predicted_weight)), 2)

            growth_rate = round(predicted_weight / 35.0, 2)
            harvest_days = 35

            return {
                "fresh_weight": predicted_weight,
                "growth_rate": growth_rate,
                "harvest_days": harvest_days,
                "confidence_score": 93.5,
                "model_version": self.version,
                "is_ml_model": True
            }
        except Exception:
            return self._fallback_prediction(features_dict)

    def _fallback_prediction(self, features: dict) -> dict:
        # Heuristic fallback calculation
        temp = features.get("air_temperature", 22.0)
        co2 = features.get("co2", 450.0)
        ph = features.get("water_ph", 6.2)
        ec = features.get("water_ec", 2.0)
        s_w = features.get("seedling_weight", 4.0)

        weight = 200.0 + (s_w * 12.0) + (co2 * 0.08)
        if temp > 28.0 or ph < 5.5 or ec > 2.5:
            weight -= 35.0

        weight = round(max(150.0, min(420.0, weight)), 2)
        return {
            "fresh_weight": weight,
            "growth_rate": round(weight / 35.0, 2),
            "harvest_days": 35,
            "confidence_score": 85.0,
            "model_version": "0.9.0-fallback",
            "is_ml_model": False
        }
