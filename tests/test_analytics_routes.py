import unittest
import os
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.authentication import jwt_handler

class TestAnalyticsRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)
        cls.db = SessionLocal()
        
        # Clear database to isolate test states
        cls.db.query(models.Prediction).delete()
        cls.db.query(models.Message).delete()
        cls.db.query(models.Conversation).delete()
        cls.db.query(models.User).delete()
        cls.db.commit()

        # Create user
        user_schema = schemas.UserCreate(
            username="routegrower",
            email="routegrower@example.com",
            password="growerpassword"
        )
        cls.user = crud.create_user(cls.db, user=user_schema, password_hash="hashed")
        cls.db.commit()

        # Generate tokens
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

    def test_unauthorized_routes_access(self):
        for endpoint in ["overview", "trends", "environment", "report", "anomalies"]:
            response = self.client.get(f"/api/analytics/{endpoint}")
            self.assertEqual(response.status_code, 401)

    def test_authorized_overview_empty(self):
        response = self.client.get("/api/analytics/overview", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_cycles"], 0)
        self.assertEqual(data["average_weight"], 0.0)

    def test_authorized_trends_and_environment(self):
        # Insert a prediction
        crud.create_prediction(
            db=self.db,
            user_id=self.user.id,
            input_parameters={"water_ph": 5.9, "water_ec": 2.0},
            predicted_weight=310.0,
            growth_category="Optimal"
        )
        self.db.commit()

        # Check trends
        response = self.client.get("/api/analytics/trends", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("weight_history", data)
        self.assertEqual(len(data["weight_history"]), 1)

        # Check environment
        response = self.client.get("/api/analytics/environment", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        env = response.json()
        self.assertEqual(env["water_ph"]["avg"], 5.9)
