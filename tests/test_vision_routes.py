import unittest
import os
from io import BytesIO
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.authentication import jwt_handler

class TestVisionRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)
        cls.db = SessionLocal()

        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="visiontester",
            email="vision@example.com",
            password="testerpassword"
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
        self.db.query(models.GrowthObservation).delete()
        self.db.commit()

    def test_unauthorized_endpoints(self):
        response = self.client.get("/api/vision/history")
        self.assertEqual(response.status_code, 401)

    def test_upload_and_analyze_healthy(self):
        dummy_file = ("lettuce_healthy.png", BytesIO(b"healthy_image_data"), "image/png")
        response = self.client.post(
            "/api/vision/analyze",
            files={"file": dummy_file},
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["disease"], "Healthy")
        self.assertGreaterEqual(data["health_score"], 90.0)

        response_hist = self.client.get("/api/vision/history", headers=self.headers)
        self.assertEqual(response_hist.status_code, 200)
        self.assertEqual(len(response_hist.json()), 1)

    def test_upload_and_analyze_tipburn(self):
        dummy_file = ("lettuce_tipburn.png", BytesIO(b"tipburn_image_data"), "image/png")
        response = self.client.post(
            "/api/vision/analyze",
            files={"file": dummy_file},
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["disease"], "Tip Burn")
