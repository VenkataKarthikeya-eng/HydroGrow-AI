"""
prediction_validation.py — HydroGrow AI Prediction Validation Layer

This module loads the training dataset or biological range fallbacks,
computes biological range parameters and percentile clipping thresholds,
and provides a validation function to flag and correct anomalous predictions.
"""

from pathlib import Path
import pandas as pd

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATASET_PATHS = [
    PROJECT_ROOT / "data" / "processed" / "final_ml_dataset.csv",
    Path("/app/data/processed/final_ml_dataset.csv"),
    CURRENT_DIR.parents[2] / "data" / "processed" / "final_ml_dataset.csv",
]

def _load_dataset_metrics():
    for p in DATASET_PATHS:
        if p.exists():
            try:
                df = pd.read_csv(p)
                TARGET_COL = "target_total_weight_g"
                if TARGET_COL in df.columns:
                    return {
                        "min": float(df[TARGET_COL].min()),
                        "max": float(df[TARGET_COL].max()),
                        "mean": float(df[TARGET_COL].mean()),
                        "p5": float(df[TARGET_COL].quantile(0.05)),
                        "p95": float(df[TARGET_COL].quantile(0.95)),
                    }
            except Exception:
                pass
    # Production fallback biological thresholds derived from hydroponic lettuce dataset
    return {
        "min": 100.0,
        "max": 450.0,
        "mean": 280.0,
        "p5": 180.0,
        "p95": 380.0,
    }

METRICS = _load_dataset_metrics()
MIN_WEIGHT = METRICS["min"]
MAX_WEIGHT = METRICS["max"]
MEAN_WEIGHT = METRICS["mean"]
P5_WEIGHT = METRICS["p5"]
P95_WEIGHT = METRICS["p95"]


def validate_prediction(prediction: float) -> dict:
    """
    Checks if a prediction is within the realistic biological range of the training data.
    If not, flags the prediction and applies percentile clipping.
    """
    original_pred = round(prediction, 2)
    
    if prediction < MIN_WEIGHT or prediction > MAX_WEIGHT:
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
