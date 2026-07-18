import unittest
import os
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.authentication import jwt_handler

class TestAutomationRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)
        cls.db = SessionLocal()

        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="routeautogrower",
            email="routeauto@example.com",
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
        self.db.query(models.CropCycle).delete()
        self.db.query(models.AutomationEvent).delete()
        self.db.query(models.AutomationRule).delete()
        self.db.commit()

    def test_unauthorized_endpoints(self):
        response = self.client.get("/api/automation/rules")
        self.assertEqual(response.status_code, 401)

        response = self.client.get("/api/crops/current")
        self.assertEqual(response.status_code, 401)

    def test_automation_rules_crud(self):
        payload = {
            "rule_name": "pH Down Pump Trigger",
            "parameter": "water_ph",
            "condition": "above",
            "threshold_value": 6.5,
            "action_type": "activate",
            "action_value": "pH Controller",
            "enabled": True
        }
        response = self.client.post("/api/automation/rules", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        rule_id = response.json()["id"]

        response = self.client.get("/api/automation/rules", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        rules = response.json()
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]["id"], rule_id)

        payload["rule_name"] = "Updated Trigger Label"
        response = self.client.put(f"/api/automation/rules/{rule_id}", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["rule_name"], "Updated Trigger Label")

        response = self.client.delete(f"/api/automation/rules/{rule_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_crop_lifecycle_endpoints(self):
        payload = {
            "crop_name": "Hydro Lettuce B",
            "expected_harvest_days": 25
        }
        response = self.client.post("/api/crops", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        cycle_id = response.json()["id"]

        response = self.client.get("/api/crops/current", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], cycle_id)
        self.assertEqual(response.json()["crop_name"], "Hydro Lettuce B")

        response = self.client.put(f"/api/crops/{cycle_id}", json={"current_stage": "Vegetative"}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["current_stage"], "Vegetative")

    def test_ai_recommendations_endpoint(self):
        response = self.client.get("/api/automation/recommendations", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("yield_improvement", response.json())
