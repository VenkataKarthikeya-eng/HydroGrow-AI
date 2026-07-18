import unittest
import os
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.authentication import jwt_handler

class TestIoTRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)
        cls.db = SessionLocal()

        # Clear existing users
        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="routeiotgrower",
            email="routeiot@example.com",
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
        self.db.query(models.Alert).delete()
        self.db.query(models.SensorReading).delete()
        self.db.query(models.SensorDevice).delete()
        self.db.commit()

    def test_unauthorized_endpoints(self):
        response = self.client.get("/api/iot/devices")
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/iot/devices", json={"device_name": "Test"})
        self.assertEqual(response.status_code, 401)

    def test_device_lifecycle(self):
        payload = {
            "device_name": "Hydro Tank 01",
            "location": "Grow Room A",
            "device_type": "Hydroponic Tank Sensor"
        }
        response = self.client.post("/api/iot/devices", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["device_name"], "Hydro Tank 01")
        device_id = data["id"]

        response = self.client.get("/api/iot/devices", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        devices = response.json()
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["id"], device_id)

        response = self.client.post(f"/api/iot/simulate?device_id={device_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        sim_res = response.json()
        self.assertIn("reading", sim_res)
        self.assertEqual(sim_res["device_id"], device_id)

        response = self.client.get(f"/api/iot/latest?device_id={device_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        latest = response.json()
        self.assertIn("water_ph", latest)
