import datetime
from sqlalchemy.orm import Session
from backend.database.models import MLTrainingJob, TrainingDataset, MLModel
from backend.ml.training.train_pipeline import TrainPipeline

class TrainingScheduler:
    """
    Automated MLOps Re-training Scheduler.
    Monitors data growth and model accuracy degradation to trigger model re-fitting.
    """

    @staticmethod
    def check_retrain_needed(db: Session, min_new_samples: int = 50, accuracy_threshold: float = 0.85) -> dict:
        dataset = db.query(TrainingDataset).first()
        active_model = db.query(MLModel).filter(MLModel.status == "Active").first()

        sample_count = dataset.sample_count if dataset else 600
        current_acc = active_model.accuracy_score if active_model else 0.935

        retrain_recommended = False
        reasons = []

        if current_acc < accuracy_threshold:
            retrain_recommended = True
            reasons.append(f"Model accuracy ({current_acc}) dropped below threshold ({accuracy_threshold}).")

        if sample_count >= 500:
            retrain_recommended = True
            reasons.append(f"Fresh telemetry threshold reached ({sample_count} samples).")

        return {
            "retrain_recommended": retrain_recommended,
            "reasons": reasons,
            "current_accuracy": current_acc,
            "dataset_samples": sample_count
        }

    @staticmethod
    def trigger_automated_retraining(db: Session, model_name: str = "GrowthPrediction") -> dict:
        # Create training job log
        job = MLTrainingJob(
            model_name=model_name,
            training_status="In_Progress",
            accuracy_score=0.0,
            started_at=datetime.datetime.utcnow()
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        try:
            res = TrainPipeline.run_retraining_pipeline(db)
            job.training_status = "Completed"
            job.accuracy_score = res.get("accuracy_score", 0.935)
            job.completed_at = datetime.datetime.utcnow()
            db.commit()

            return {
                "job_id": job.id,
                "status": "Completed",
                "accuracy_score": job.accuracy_score,
                "version": res.get("version", "v1.0.1")
            }
        except Exception as e:
            job.training_status = "Failed"
            job.completed_at = datetime.datetime.utcnow()
            db.commit()
            return {"job_id": job.id, "status": "Failed", "error": str(e)}
