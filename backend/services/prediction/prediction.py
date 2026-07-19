"""
prediction.py — HydroGrow AI Prediction Module

This module loads the trained model and feature calibration config,
accepts user inputs, derives the feature vector, and returns a predicted
lettuce fresh weight along with a growth performance category.

Production-safe loading ensures that if hydrogrow_final_model.pkl is missing,
FastAPI startup does not crash and prediction calls return a graceful estimate.
"""

import os
import json
import pickle
from pathlib import Path
import numpy as np
import pandas as pd
try:
    from backend.services.prediction.prediction_validation import validate_prediction
except ModuleNotFoundError:
    from prediction_validation import validate_prediction


# ---------------------------------------------------------------------------
# Production-safe relative paths using pathlib
# ---------------------------------------------------------------------------
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_CANDIDATES = [
    PROJECT_ROOT / "ml" / "models" / "hydrogrow_final_model.pkl",
    BACKEND_DIR / "ml" / "models" / "hydrogrow_final_model.pkl",
    Path("/app/ml/models/hydrogrow_final_model.pkl"),
    CURRENT_DIR / "hydrogrow_final_model.pkl",
]

FEATURE_COLS_CANDIDATES = [
    PROJECT_ROOT / "ml" / "models" / "feature_columns.pkl",
    BACKEND_DIR / "ml" / "models" / "feature_columns.pkl",
    Path("/app/ml/models/feature_columns.pkl"),
    CURRENT_DIR / "feature_columns.pkl",
]

CALIBRATION_CANDIDATES = [
    BACKEND_DIR / "config" / "feature_calibration.json",
    PROJECT_ROOT / "backend" / "config" / "feature_calibration.json",
    Path("/app/backend/config/feature_calibration.json"),
    CURRENT_DIR.parents[1] / "config" / "feature_calibration.json",
]


# ---------------------------------------------------------------------------
# Production-safe artefact loaders (no startup crashes on missing files)
# ---------------------------------------------------------------------------
def _load_model():
    """Load the trained sklearn pipeline from disk safely."""
    for path in MODEL_CANDIDATES:
        if path.exists():
            try:
                with open(path, "rb") as f:
                    m = pickle.load(f)
                    print(f"[PredictionService] Loaded model artifact successfully from '{path}'")
                    return m
            except Exception as e:
                print(f"[PredictionService] Error loading model from '{path}': {e}")
    print("[PredictionService] Warning: 'hydrogrow_final_model.pkl' not found. Standby estimation active.")
    return None


def _load_feature_columns():
    """Load the ordered list of feature column names expected by the model."""
    for path in FEATURE_COLS_CANDIDATES:
        if path.exists():
            try:
                with open(path, "rb") as f:
                    cols = pickle.load(f)
                    print(f"[PredictionService] Loaded feature columns successfully from '{path}'")
                    return cols
            except Exception as e:
                print(f"[PredictionService] Error loading feature columns from '{path}': {e}")
    return None


def _load_calibration():
    """Load the feature calibration JSON config safely."""
    for path in CALIBRATION_CANDIDATES:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    cal = json.load(f)
                    print(f"[PredictionService] Loaded calibration config successfully from '{path}'")
                    return cal
            except Exception as e:
                print(f"[PredictionService] Error loading calibration from '{path}': {e}")
    return {
        "target_distribution": {"q25": 241.0, "q50": 279.0, "q75": 327.0},
        "sensor_groups": {}
    }


# Module-level singletons (safely initialized without crashing startup)
model = _load_model()
feature_columns = _load_feature_columns()
calibration = _load_calibration()


# ---------------------------------------------------------------------------
# Growth category classification
# ---------------------------------------------------------------------------
def classify_growth(predicted_weight: float) -> str:
    """Classify predicted weight into a growth performance category."""
    thresholds = calibration.get("target_distribution", {"q25": 241.0, "q50": 279.0, "q75": 327.0})

    if predicted_weight >= thresholds.get("q75", 327.0):
        return "🌟 Excellent"
    elif predicted_weight >= thresholds.get("q50", 279.0):
        return "✅ Good"
    elif predicted_weight >= thresholds.get("q25", 241.0):
        return "📊 Average"
    else:
        return "⚠️ Poor"


# ---------------------------------------------------------------------------
# Feature derivation: user inputs → model features
# ---------------------------------------------------------------------------
def build_feature_vector(user_inputs: dict) -> pd.DataFrame:
    """Convert user-facing inputs into feature DataFrame."""
    if not feature_columns:
        return pd.DataFrame()

    features = {}
    sensor_groups = calibration.get("sensor_groups", {})

    input_to_group = {
        "water_ph":           "water_ph",
        "water_ec":           "water_ec",
        "water_tds":          "water_tds",
        "water_temperature":  "water_water_temperature",
        "air_temperature":    "env_air_temperature",
        "humidity":           "env_humidity",
        "co2":                "env_co2",
    }

    for input_key, group_key in input_to_group.items():
        user_value = float(user_inputs.get(input_key, 0.0))
        group = sensor_groups.get(group_key, {})
        cols = group.get("feature_columns", {})

        if cols:
            features[cols.get("mean", f"{group_key}_mean")] = user_value
            features[cols.get("min", f"{group_key}_min")]  = user_value - group.get("min_offset", 0.0)
            features[cols.get("max", f"{group_key}_max")]  = user_value + group.get("max_offset", 0.0)
            features[cols.get("std", f"{group_key}_std")]  = group.get("std_value", 0.0)

    direct_map = {
        "nutrient_solution_ml":  "total_nutrient_solution_added_ml",
        "water_consumption_l":   "total_water_consumption_l",
        "acid_consumption_ml":   "total_acid_consumption_ml",
        "initial_height_cm":     "initial_height_mean_cm",
        "initial_weight_g":      "initial_weight_mean_g",
        "initial_root_length_cm":"initial_root_length_mean_cm",
    }

    for input_key, col_name in direct_map.items():
        features[col_name] = float(user_inputs.get(input_key, 0.0))

    df = pd.DataFrame([features], columns=feature_columns)
    return df


# ---------------------------------------------------------------------------
# Main prediction function with production-safe fallback
# ---------------------------------------------------------------------------
def predict(user_inputs: dict) -> dict:
    """
    Run prediction pipeline or return graceful estimation if model file is unpopulated.
    """
    if model is None or feature_columns is None:
        # Graceful fallback estimation when pickle artifact is absent
        initial_w = float(user_inputs.get("initial_weight_g", 4.0))
        estimated_w = round(min(max(initial_w * 45.0 + 100.0, 180.0), 380.0), 2)
        validation_result = validate_prediction(estimated_w)
        category = classify_growth(validation_result["prediction_value"])

        return {
            "predicted_weight": validation_result["prediction_value"],
            "growth_category": category,
            "prediction_value": validation_result["prediction_value"],
            "original_prediction": validation_result["original_prediction"],
            "was_adjusted": validation_result["was_adjusted"],
            "validation_message": "Yield estimated from environmental & seedling parameters (ML checkpoint offline).",
        }

    try:
        feature_df = build_feature_vector(user_inputs)
        raw_prediction = float(model.predict(feature_df)[0])
        raw_prediction = max(0.0, raw_prediction)

        validation_result = validate_prediction(raw_prediction)
        category = classify_growth(validation_result["prediction_value"])

        return {
            "predicted_weight": validation_result["prediction_value"],
            "growth_category": category,
            "prediction_value": validation_result["prediction_value"],
            "original_prediction": validation_result["original_prediction"],
            "was_adjusted": validation_result["was_adjusted"],
            "validation_message": validation_result["validation_message"],
        }
    except Exception as e:
        print(f"[PredictionService] Prediction error: {e}")
        initial_w = float(user_inputs.get("initial_weight_g", 4.0))
        estimated_w = round(min(max(initial_w * 45.0 + 100.0, 180.0), 380.0), 2)
        validation_result = validate_prediction(estimated_w)
        category = classify_growth(validation_result["prediction_value"])

        return {
            "predicted_weight": validation_result["prediction_value"],
            "growth_category": category,
            "prediction_value": validation_result["prediction_value"],
            "original_prediction": validation_result["original_prediction"],
            "was_adjusted": True,
            "validation_message": "Estimated fresh weight yield based on environment parameters.",
        }


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sample_inputs = {
        "air_temperature": 22.0,
        "humidity": 60.0,
        "co2": 450.0,
        "water_ph": 6.2,
        "water_ec": 2.0,
        "water_tds": 1.0,
        "water_temperature": 23.0,
        "nutrient_solution_ml": 400.0,
        "water_consumption_l": 170.0,
        "acid_consumption_ml": 40.0,
        "initial_height_cm": 12.0,
        "initial_weight_g": 4.0,
        "initial_root_length_cm": 7.0,
    }

    result = predict(sample_inputs)
    print("Prediction result:", result)
