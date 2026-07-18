from sqlalchemy.orm import Session
from backend.database.models import Greenhouse

class GreenhouseManager:
    """
    Greenhouse Infrastructure & Growing Environment Manager.
    """

    @classmethod
    def create_greenhouse(
        cls, 
        db: Session, 
        farm_id: int, 
        name: str, 
        area_size: float = 50.0,
        environment_type: str = "NFT Hydroponics"
    ) -> Greenhouse:
        gh = Greenhouse(
            farm_id=farm_id,
            name=name,
            area_size=area_size,
            environment_type=environment_type,
            automation_enabled=True
        )
        db.add(gh)
        db.commit()
        db.refresh(gh)
        return gh

    @classmethod
    def list_greenhouses(cls, db: Session, farm_id: int) -> list:
        return db.query(Greenhouse).filter(Greenhouse.farm_id == farm_id).all()

    @classmethod
    def get_greenhouse_status(cls, db: Session, greenhouse_id: int) -> dict:
        gh = db.query(Greenhouse).filter(Greenhouse.id == greenhouse_id).first()
        if not gh:
            return None
        return {
            "id": gh.id,
            "farm_id": gh.farm_id,
            "name": gh.name,
            "area_size": gh.area_size,
            "environment_type": gh.environment_type,
            "automation_enabled": gh.automation_enabled,
            "status": "Optimal",
            "health_score": 94.5
        }
