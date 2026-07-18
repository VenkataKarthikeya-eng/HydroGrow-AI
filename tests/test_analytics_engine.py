import unittest
import os
from sqlalchemy.orm import Session
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.services.analytics.analytics_engine import AnalyticsEngine

class TestAnalyticsEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()
        
        # Clear database users
        cls.db.query(models.User).delete()
        cls.db.commit()

        # Create user
        user_schema = schemas.UserCreate(
            username="analyticsgrower",
            email="analyticsgrower@example.com",
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
        # Clear predictions and conversations before each test run
        self.db.query(models.Prediction).delete()
        self.db.query(models.Conversation).delete()
        self.db.commit()

    def test_zero_predictions_statistics(self):
        stats = AnalyticsEngine.get_user_statistics(self.db, self.user.id)
        self.assertEqual(stats["total_predictions"], 0)
        self.assertEqual(stats["average_weight"], 0.0)
        self.assertEqual(stats["best_prediction"], 0.0)
        self.assertEqual(stats["success_rate"], 0.0)

        env = AnalyticsEngine.get_environment_statistics(self.db, self.user.id)
        self.assertEqual(env["water_ph"]["avg"], 0.0)
        
        performance = AnalyticsEngine.get_growth_performance(self.db, self.user.id)
        self.assertEqual(len(performance), 0)

    def test_prediction_statistics_aggregation(self):
        # Insert mock prediction values
        crud.create_prediction(
            db=self.db,
            user_id=self.user.id,
            input_parameters={"water_ph": 6.0, "water_ec": 2.0, "air_temperature": 22.0, "humidity": 60.0, "co2": 450.0, "water_temperature": 21.0},
            predicted_weight=300.0,
            growth_category="Optimal"
        )
        crud.create_prediction(
            db=self.db,
            user_id=self.user.id,
            input_parameters={"water_ph": 5.8, "water_ec": 2.2, "air_temperature": 21.0, "humidity": 65.0, "co2": 480.0, "water_temperature": 20.0},
            predicted_weight=350.0,
            growth_category="Excellent"
        )
        crud.create_prediction(
            db=self.db,
            user_id=self.user.id,
            input_parameters={"water_ph": 4.5, "water_ec": 1.2, "air_temperature": 29.0, "humidity": 55.0, "co2": 350.0, "water_temperature": 25.0},
            predicted_weight=150.0,
            growth_category="Poor"
        )
        self.db.commit()

        stats = AnalyticsEngine.get_user_statistics(self.db, self.user.id)
        self.assertEqual(stats["total_predictions"], 3)
        self.assertEqual(stats["best_prediction"], 350.0)
        self.assertEqual(stats["average_weight"], 266.7)
        self.assertEqual(stats["success_rate"], 66.7)

        env = AnalyticsEngine.get_environment_statistics(self.db, self.user.id)
        self.assertEqual(env["water_ph"]["avg"], 5.43)
        self.assertEqual(env["water_ph"]["min"], 4.5)
        self.assertEqual(env["water_ph"]["max"], 6.0)
