from sqlalchemy.orm import Session
from backend.database.models import MLModel

class ModelRegistry:
    """
    MLOps Production Model Version & Deployment Registry Manager.
    """

    @staticmethod
    def list_models(db: Session) -> list:
        models = db.query(MLModel).order_by(MLModel.created_at.desc()).all()
        return [
            {
                "id": m.id,
                "model_name": m.model_name,
                "version": m.version,
                "algorithm": m.algorithm,
                "accuracy_score": m.accuracy_score,
                "status": m.status,
                "created_at": m.created_at.isoformat() if m.created_at else None
            }
            for m in models
        ]

    @staticmethod
    def promote_to_active(db: Session, model_id: int) -> dict:
        target = db.query(MLModel).filter(MLModel.id == model_id).first()
        if not target:
            return {"status": "error", "message": "Model ID not found."}

        # Archive other active models of same type
        other_active = db.query(MLModel).filter(
            MLModel.model_name == target.model_name,
            MLModel.id != model_id
        ).all()
        for m in other_active:
            m.status = "Archived"

        target.status = "Active"
        db.commit()

        return {
            "status": "success",
            "active_version": target.version,
            "model_name": target.model_name
        }
