import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score

class ModelMetrics:
    """
    Evaluation metrics calculator for regression and classification models.
    """

    @staticmethod
    def evaluate_regression(y_true: list, y_pred: list) -> dict:
        y_t = np.array(y_true)
        y_p = np.array(y_pred)
        mae = float(mean_absolute_error(y_t, y_p))
        rmse = float(np.sqrt(mean_squared_error(y_t, y_p)))
        r2 = float(r2_score(y_t, y_p))

        return {
            "mae": round(mae, 3),
            "rmse": round(rmse, 3),
            "r2_score": round(r2, 4),
            "accuracy_score": round(max(0.0, r2), 4)
        }

    @staticmethod
    def evaluate_classification(y_true: list, y_pred: list) -> dict:
        y_t = np.array(y_true)
        y_p = np.array(y_pred)
        acc = float(accuracy_score(y_t, y_p))
        prec = float(precision_score(y_t, y_p, average="weighted", zero_division=0))
        rec = float(recall_score(y_t, y_p, average="weighted", zero_division=0))
        f1 = float(f1_score(y_t, y_p, average="weighted", zero_division=0))

        return {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4)
        }
