import unittest
import os
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.services.analytics.anomaly_detector import AnomalyDetector

class TestAnomalyDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()
        
        # Clear database users
        cls.db.query(models.User).delete()
        cls.db.commit()

        # Create user
        user_schema = schemas.UserCreate(
            username="anomalygrower",
            email="anomalygrower@example.com",
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
        # Clear predictions and conversations before each test
        self.db.query(models.Prediction).delete()
        self.db.query(models.Conversation).delete()
        self.db.commit()

    def test_no_anomalies_initially(self):
        alerts = AnomalyDetector.detect_anomalies(self.db, self.user.id)
        self.assertEqual(len(alerts), 0)

    def test_detect_sudden_yield_drop(self):
        # Insert a high weight cycle
        crud.create_prediction(
            db=self.db,
            user_id=self.user.id,
            input_parameters={"water_ph": 6.0},
            predicted_weight=350.0,
            growth_category="Optimal"
        )
        # Insert a low weight cycle (>20% decline)
        crud.create_prediction(
            db=self.db,
            user_id=self.user.id,
            input_parameters={"water_ph": 6.0},
            predicted_weight=200.0,
            growth_category="Poor"
        )
        self.db.commit()

        alerts = AnomalyDetector.detect_anomalies(self.db, self.user.id)
        alert_titles = [a["alert"] for a in alerts]
        self.assertIn("Sudden yield drop detected", alert_titles)

    def test_detect_extreme_environmental_temperature(self):
        # Insert abnormal high temperature prediction run
        crud.create_prediction(
            db=self.db,
            user_id=self.user.id,
            input_parameters={"air_temperature": 32.0},
            predicted_weight=210.0,
            growth_category="Poor"
        )
        self.db.commit()

        alerts = AnomalyDetector.detect_anomalies(self.db, self.user.id)
        alert_titles = [a["alert"] for a in alerts]
        self.assertIn("Abnormal grow room temperature", alert_titles)
