import unittest
import os
from datetime import datetime, timedelta
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.services.automation.crop_lifecycle_manager import CropLifecycleManager

class TestCropLifecycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()

        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="lifecyclecropgrower",
            email="lifecycle@example.com",
            password="growerpassword"
        )
        cls.user = crud.create_user(cls.db, user=user_schema, password_hash="hashed")
        cls.db.commit()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("test_hydrogrow.db"):
            try:
                os.remove("test_hydrogrow.db")
            except Exception:
                pass

    def setUp(self):
        self.db.query(models.CropCycle).delete()
        self.db.commit()

    def test_create_crop_cycle(self):
        cycle = CropLifecycleManager.create_crop_cycle(
            db=self.db,
            user_id=self.user.id,
            crop_name="Romaine Lettuce",
            expected_harvest_days=30
        )
        self.assertEqual(cycle.crop_name, "Romaine Lettuce")
        self.assertEqual(cycle.current_stage, "Seedling")
        self.assertEqual(cycle.status, "active")

    def test_advance_and_harvest(self):
        cycle = CropLifecycleManager.create_crop_cycle(
            db=self.db,
            user_id=self.user.id,
            crop_name="Oakleaf Lettuce"
        )

        updated = CropLifecycleManager.update_growth_stage(self.db, self.user.id, cycle.id, "Vegetative")
        self.assertEqual(updated.current_stage, "Vegetative")

        updated = CropLifecycleManager.update_growth_stage(self.db, self.user.id, cycle.id, "Harvest")
        self.assertEqual(updated.current_stage, "Harvest")
        self.assertEqual(updated.status, "completed")
        self.assertEqual(updated.growth_progress, 100.0)

    def test_calculate_growth_progress(self):
        start = datetime.utcnow() - timedelta(days=15)
        harvest = datetime.utcnow() + timedelta(days=15)
        prog = CropLifecycleManager.calculate_growth_progress(start, harvest)
        self.assertAlmostEqual(prog, 50.0, places=1)
