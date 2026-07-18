from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.database.models import CropCycle

class CropLifecycleManager:
    """
    Manages crop lifecycle phases, start times, expected harvest metrics,
    and progress calculations.
    """
    @staticmethod
    def create_crop_cycle(
        db: Session, 
        user_id: int, 
        crop_name: str, 
        start_date: datetime = None,
        expected_harvest_days: int = 30
    ) -> CropCycle:
        if not start_date:
            start_date = datetime.utcnow()
            
        expected_harvest_date = start_date + timedelta(days=expected_harvest_days)
        
        cycle = CropCycle(
            user_id=user_id,
            crop_name=crop_name,
            start_date=start_date,
            current_stage="Seedling",
            expected_harvest_date=expected_harvest_date,
            growth_progress=0.0,
            status="active"
        )
        db.add(cycle)
        db.commit()
        db.refresh(cycle)
        return cycle

    @staticmethod
    def update_growth_stage(
        db: Session, 
        user_id: int, 
        cycle_id: int, 
        new_stage: str
    ) -> CropCycle:
        cycle = db.query(CropCycle).filter(
            CropCycle.id == cycle_id,
            CropCycle.user_id == user_id
        ).first()

        if not cycle:
            raise ValueError("Crop cycle not found or access denied.")

        if new_stage not in ["Seedling", "Vegetative", "Maturity", "Harvest"]:
            raise ValueError(f"Invalid growth stage: {new_stage}")

        cycle.current_stage = new_stage
        
        if new_stage == "Harvest":
            cycle.status = "completed"
            cycle.growth_progress = 100.0
            
        db.commit()
        db.refresh(cycle)
        return cycle

    @staticmethod
    def calculate_growth_progress(start_date: datetime, expected_harvest_date: datetime) -> float:
        now = datetime.utcnow()
        if now <= start_date:
            return 0.0
        if now >= expected_harvest_date:
            return 100.0
            
        total_duration = (expected_harvest_date - start_date).total_seconds()
        elapsed_duration = (now - start_date).total_seconds()
        
        if total_duration <= 0:
            return 100.0
            
        progress = (elapsed_duration / total_duration) * 100.0
        return round(max(0.0, min(100.0, progress)), 2)
