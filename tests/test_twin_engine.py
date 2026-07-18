import unittest
from backend.database.connection import SessionLocal, engine, Base
from backend.database import models
from backend.services.digital_twin.twin_engine import TwinEngine

class TestTwinEngine(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
        # Seed test user
        self.user = self.db.query(models.User).filter(models.User.email == "test_twin@hydrogrow.ai").first()
        if not self.user:
            self.user = models.User(
                username="testtwinuser",
                email="test_twin@hydrogrow.ai",
                password_hash="mockhashedpassword"
            )
            self.db.add(self.user)
            self.db.commit()
            self.db.refresh(self.user)

    def tearDown(self):
        self.db.query(models.DigitalTwinProfile).filter(models.DigitalTwinProfile.user_id == self.user.id).delete()
        self.db.commit()
        self.db.close()

    def test_create_virtual_profile(self):
        profile = TwinEngine.create_virtual_profile(
            self.db,
            user_id=self.user.id,
            farm_name="Twin Greenhouse",
            system_type="Drip Irrigation",
            area_size=40.0,
            lighting_setup="High Pressure Sodium",
            nutrient_system="Manual Dose"
        )
        self.assertEqual(profile.farm_name, "Twin Greenhouse")
        self.assertEqual(profile.system_type, "Drip Irrigation")

    def test_resolve_farm_baseline_conditions_fallback(self):
        conds = TwinEngine.resolve_farm_baseline_conditions(self.db, self.user.id)
        self.assertEqual(conds["temperature"], 22.0)
        self.assertEqual(conds["water_ec"], 2.0)
