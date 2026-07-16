"""
prediction.py — HydroGrow AI Prediction Module

This module loads the trained model and feature calibration config,
accepts simplified user inputs (13 values), derives the full 34-feature
vector using data-driven calibration offsets, and returns a predicted
lettuce fresh weight along with a growth performance category.

The model is NOT retrained here. We only load and use the saved pipeline.
"""

import os
import json
import pickle
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Paths (relative to backend/services/prediction/ directory)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "..", "ml", "models", "hydrogrow_final_model.pkl"))
FEATURE_COLS_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "..", "ml", "models", "feature_columns.pkl"))
CALIBRATION_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "config", "feature_calibration.json"))


# ---------------------------------------------------------------------------
# Load artefacts once at import time
# ---------------------------------------------------------------------------
def _load_model():
    """Load the trained sklearn pipeline from disk."""
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model


def _load_feature_columns():
    """Load the ordered list of feature column names expected by the model."""
    with open(FEATURE_COLS_PATH, "rb") as f:
        columns = pickle.load(f)
    return columns


def _load_calibration():
    """Load the feature calibration JSON config."""
    with open(CALIBRATION_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


# Module-level singletons (loaded once when the module is first imported)
model = _load_model()
feature_columns = _load_feature_columns()
calibration = _load_calibration()


# ---------------------------------------------------------------------------
# Growth category classification based on training data quartiles
# ---------------------------------------------------------------------------
from backend.services.prediction.prediction_validation import validate_prediction


# ---------------------------------------------------------------------------
# Growth category classification based on training data quartiles
# ---------------------------------------------------------------------------
def classify_growth(predicted_weight: float) -> str:
    """
    Classify predicted weight into a growth performance category
    using quartile thresholds from the training target distribution.

    Thresholds (from final_ml_dataset.csv):
        Q25 = 241 g, Q50 = 279 g, Q75 = 327 g
    """
    thresholds = calibration["target_distribution"]

    if predicted_weight >= thresholds["q75"]:
        return "🌟 Excellent"
    elif predicted_weight >= thresholds["q50"]:
        return "✅ Good"
    elif predicted_weight >= thresholds["q25"]:
        return "📊 Average"
    else:
        return "⚠️ Poor"


# ---------------------------------------------------------------------------
# Feature derivation: 13 user inputs → 34 model features
# ---------------------------------------------------------------------------
def build_feature_vector(user_inputs: dict) -> pd.DataFrame:
    """
    Convert 13 user-facing inputs into the full 34-feature DataFrame
    expected by the trained model.

    Statistical features (min, max, std) are derived from the user's
    representative 'mean' value using calibration offsets learned from
    the training dataset distribution.

    Parameters
    ----------
    user_inputs : dict
        Keys must include:
            water_ph, water_ec, water_tds, water_temperature,
            air_temperature, humidity, co2,
            nutrient_solution_ml, water_consumption_l, acid_consumption_ml,
            initial_height_cm, initial_weight_g, initial_root_length_cm

    Returns
    -------
    pd.DataFrame with one row and 34 columns in the exact order
    expected by the model.
    """
    features = {}
    sensor_groups = calibration["sensor_groups"]

    # --- Map user input keys to calibration group keys ---
    input_to_group = {
        "water_ph":           "water_ph",
        "water_ec":           "water_ec",
        "water_tds":          "water_tds",
        "water_temperature":  "water_water_temperature",
        "air_temperature":    "env_air_temperature",
        "humidity":           "env_humidity",
        "co2":                "env_co2",
    }

    # Derive mean/min/max/std for each sensor group
    for input_key, group_key in input_to_group.items():
        user_value = float(user_inputs[input_key])
        group = sensor_groups[group_key]
        cols = group["feature_columns"]

        # mean = user's representative value
        features[cols["mean"]] = user_value
        # min  = mean - median offset from training data
        features[cols["min"]]  = user_value - group["min_offset"]
        # max  = mean + median offset from training data
        features[cols["max"]]  = user_value + group["max_offset"]
        # std  = median std value from training data
        features[cols["std"]]  = group["std_value"]

    # --- Direct features (no derivation needed) ---
    direct_map = {
        "nutrient_solution_ml":  "total_nutrient_solution_added_ml",
        "water_consumption_l":   "total_water_consumption_l",
        "acid_consumption_ml":   "total_acid_consumption_ml",
        "initial_height_cm":     "initial_height_mean_cm",
        "initial_weight_g":      "initial_weight_mean_g",
        "initial_root_length_cm":"initial_root_length_mean_cm",
    }

    for input_key, col_name in direct_map.items():
        features[col_name] = float(user_inputs[input_key])

    # Build a single-row DataFrame with columns in the exact model order
    df = pd.DataFrame([features], columns=feature_columns)
    return df


# ---------------------------------------------------------------------------
# Main prediction function
# ---------------------------------------------------------------------------
def predict(user_inputs: dict) -> dict:
    """
    Run the full prediction pipeline.

    Parameters
    ----------
    user_inputs : dict
        The 13 user-facing input values (see build_feature_vector).

    Returns
    -------
    dict with keys:
        predicted_weight    : float  — predicted/validated fresh weight in grams
        growth_category     : str    — Excellent / Good / Average / Poor
        prediction_value    : float  — validated weight in grams
        original_prediction : float  — raw model prediction in grams
        was_adjusted        : bool   — true if prediction was clipped
        validation_message  : str    — validation result description
    """
    # Step 1: Build the 34-feature vector
    feature_df = build_feature_vector(user_inputs)

    # Step 2: Predict using the loaded pipeline (scaler + model)
    raw_prediction = float(model.predict(feature_df)[0])

    # Ensure prediction is non-negative (physical constraint)
    raw_prediction = max(0.0, raw_prediction)

    # Step 3: Apply Prediction Validation Layer
    validation_result = validate_prediction(raw_prediction)

    # Step 4: Classify growth category using the validated weight
    category = classify_growth(validation_result["prediction_value"])

    return {
        "predicted_weight": validation_result["prediction_value"],
        "growth_category": category,
        "prediction_value": validation_result["prediction_value"],
        "original_prediction": validation_result["original_prediction"],
        "was_adjusted": validation_result["was_adjusted"],
        "validation_message": validation_result["validation_message"],
    }


# ---------------------------------------------------------------------------
# Standalone test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Sample inputs representing a typical healthy lettuce growth scenario
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

    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 50)
    print("HydroGrow AI — Prediction Module Test")
    print("=" * 50)
    print(f"\nModel loaded: {type(model).__name__}")
    print(f"Feature count: {len(feature_columns)}")
    print(f"\nSample inputs: {json.dumps(sample_inputs, indent=2)}")

    result = predict(sample_inputs)

    print(f"\n--- Prediction Result ---")
    print(f"Predicted Fresh Weight: {result['predicted_weight']} g")
    print(f"Growth Category:        {result['growth_category']}")
    print("\nPrediction module test passed!")
