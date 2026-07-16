"""
prediction_validation.py — HydroGrow AI Prediction Validation Layer

This module loads the training dataset, computes biological range parameters (min, max, mean)
and percentile clipping thresholds (5th and 95th percentiles), and provides a validation
function to flag and correct anomalous lettuce weight predictions.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "..", "data", "processed", "final_ml_dataset.csv"))

# Load dataset and calculate metrics at module import time
if os.path.exists(DATASET_PATH):
    df = pd.read_csv(DATASET_PATH)
    TARGET_COL = "target_total_weight_g"
    
    if TARGET_COL in df.columns:
        MIN_WEIGHT = float(df[TARGET_COL].min())
        MAX_WEIGHT = float(df[TARGET_COL].max())
        MEAN_WEIGHT = float(df[TARGET_COL].mean())
        P5_WEIGHT = float(df[TARGET_COL].quantile(0.05))
        P95_WEIGHT = float(df[TARGET_COL].quantile(0.95))
    else:
        raise KeyError(f"Target column '{TARGET_COL}' not found in training dataset at {DATASET_PATH}")
else:
    raise FileNotFoundError(f"Training dataset not found at expected location: {DATASET_PATH}")


def validate_prediction(prediction: float) -> dict:
    """
    Checks if a prediction is within the realistic biological range of the training data.
    If not, flags the prediction and applies percentile clipping (5th and 95th percentiles).

    Parameters
    ----------
    prediction : float
        The predicted weight value in grams.

    Returns
    -------
    dict
        A dictionary containing:
        - prediction_value: float (the final validated/corrected prediction)
        - original_prediction: float (the raw model prediction)
        - was_adjusted: bool (indicating if clipping was applied)
        - validation_message: str (explanation of the validation outcome)
    """
    # Round predictions to 2 decimal places for consistency
    original_pred = round(prediction, 2)
    
    # Check if prediction is outside the realistic biological range [MIN_WEIGHT, MAX_WEIGHT]
    if prediction < MIN_WEIGHT or prediction > MAX_WEIGHT:
        # Apply safe correction using percentile clipping
        clipped_val = max(P5_WEIGHT, min(prediction, P95_WEIGHT))
        prediction_value = round(clipped_val, 2)
        was_adjusted = True
        validation_message = "Prediction was outside biological range and was corrected."
    else:
        prediction_value = original_pred
        was_adjusted = False
        validation_message = "Valid prediction"
        
    return {
        "prediction_value": prediction_value,
        "original_prediction": original_pred,
        "was_adjusted": was_adjusted,
        "validation_message": validation_message
    }
