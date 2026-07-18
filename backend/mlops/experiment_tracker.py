import datetime

class ExperimentTracker:
    """
    MLOps Experiment Tracking & Hyperparameter Logger.
    """

    def __init__(self):
        self.experiments = [
            {
                "experiment_id": "exp_001",
                "model_name": "RandomForestRegressor",
                "n_estimators": 100,
                "max_depth": 12,
                "r2_score": 0.935,
                "mae": 12.4,
                "timestamp": (datetime.datetime.utcnow() - datetime.timedelta(days=2)).isoformat()
            },
            {
                "experiment_id": "exp_002",
                "model_name": "GradientBoostingRegressor",
                "n_estimators": 150,
                "learning_rate": 0.05,
                "r2_score": 0.941,
                "mae": 11.2,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
        ]

    def log_experiment(self, params: dict, metrics: dict) -> dict:
        exp_id = f"exp_{len(self.experiments) + 1:03d}"
        entry = {
            "experiment_id": exp_id,
            "params": params,
            "metrics": metrics,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        self.experiments.append(entry)
        return entry

    def list_experiments(self) -> list:
        return self.experiments

tracker_instance = ExperimentTracker()
