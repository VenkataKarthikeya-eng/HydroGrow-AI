import unittest
import os
from io import BytesIO
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.authentication import jwt_handler
from backend.services.automation.action_simulator import ActionSimulator

class TestVisionAutomation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)
        cls.db = SessionLocal()

        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="visionautogrower",
            email="visionauto@example.com",
            password="growerpassword"
        )
        cls.user = crud.create_user(cls.db, user=user_schema, password_hash="hashed")
        cls.db.commit()

        cls.token = jwt_handler.create_access_token({"sub": cls.user.username, "user_id": cls.user.id})
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

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
        self.db.query(models.PlantImage).delete()
        self.db.query(models.PlantAnalysis).delete()
        self.db.query(models.AutomationEvent).delete()
        self.db.commit()

    def test_tipburn_actuator_reduction_trigger(self):
        ActionSimulator.simulate_action("Nutrient Pump", "activate", "Initial State Setup")
        self.assertEqual(ActionSimulator.get_device_status("Nutrient Pump"), "active")

        dummy_file = ("lettuce_tipburn.png", BytesIO(b"tipburn_data"), "image/png")
        response = self.client.post(
            "/api/vision/analyze",
            files={"file": dummy_file},
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(ActionSimulator.get_device_status("Nutrient Pump"), "inactive")

        events = self.db.query(models.AutomationEvent).filter(models.AutomationEvent.user_id == self.user.id).all()
        self.assertTrue(any("Nutrient Pump" in ev.message for ev in events))

    def test_critical_health_alert_trigger(self):
        dummy_file = ("lettuce_rootrot.png", BytesIO(b"rootrot_data"), "image/png")
        response = self.client.post(
            "/api/vision/analyze",
            files={"file": dummy_file},
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertLess(response.json()["health_score"], 50.0)

        events = self.db.query(models.AutomationEvent).filter(
            models.AutomationEvent.user_id == self.user.id,
            models.AutomationEvent.event_type == "plant_health_alert"
        ).all()
        self.assertEqual(len(events), 1)
