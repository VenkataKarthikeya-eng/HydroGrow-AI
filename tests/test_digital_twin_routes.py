import unittest
import os
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.authentication import jwt_handler

class TestDigitalTwinRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)
        cls.db = SessionLocal()

        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="twintester",
            email="twin@example.com",
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
        self.db.query(models.DigitalTwinProfile).delete()
        self.db.query(models.SimulationRun).delete()
        self.db.commit()

    def test_unauthorized_endpoints(self):
        response = self.client.get("/api/twin/history")
        self.assertEqual(response.status_code, 401)

    def test_create_and_simulate_runs(self):
        # 1. Create Profile
        profile_data = {
            "farm_name": "Test Twin Farm 01",
            "system_type": "NFT Hydroponics",
            "area_size": 25.5,
            "lighting_setup": "LED Lighting",
            "nutrient_system": "Auto Nutrient Pump"
        }
        res_create = self.client.post("/api/twin/create", json=profile_data, headers=self.headers)
        self.assertEqual(res_create.status_code, 200)
        self.assertEqual(res_create.json()["farm_name"], "Test Twin Farm 01")

        # 2. Run simulation
        sim_data = {
            "scenario_name": "EC Nutrient Dosing Increase",
            "duration_days": 10,
            "overrides": {
                "water_ec": 2.2,
                "temperature": 23.0
            }
        }
        res_sim = self.client.post("/api/twin/simulate", json=sim_data, headers=self.headers)
        self.assertEqual(res_sim.status_code, 200)
        data = res_sim.json()
        self.assertIn("simulation_id", data)
        self.assertGreater(data["harvest_prediction"]["expected_weight"], 0.0)

        # 3. Get Forecast details
        sim_id = data["simulation_id"]
        res_fc = self.client.get(f"/api/twin/forecast/{sim_id}", headers=self.headers)
        self.assertEqual(res_fc.status_code, 200)
        self.assertEqual(len(res_fc.json()), 10)

        # 4. Scenario comparisons
        compare_data = {
            "original_conditions": {"temperature": 22.0, "water_ec": 2.0},
            "modified_conditions": {"temperature": 23.0, "water_ec": 2.2},
            "duration_days": 10
        }
        res_compare = self.client.post("/api/twin/compare", json=compare_data, headers=self.headers)
        self.assertEqual(res_compare.status_code, 200)
        self.assertIn("yield_difference", res_compare.json())

        # 5. History run logs list
        res_hist = self.client.get("/api/twin/history", headers=self.headers)
        self.assertEqual(res_hist.status_code, 200)
        self.assertEqual(len(res_hist.json()), 1)

        # 6. Recommendations list
        res_recs = self.client.get("/api/twin/recommendations", headers=self.headers)
        self.assertEqual(res_recs.status_code, 200)
        self.assertGreater(len(res_recs.json()), 0)
