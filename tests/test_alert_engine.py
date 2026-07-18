import unittest
import os
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.services.iot.alert_engine import AlertEngine

class TestAlertEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()

        # Clear existing users
        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="alertgrower",
            email="alert@example.com",
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
        self.db.query(models.Alert).delete()
        self.db.commit()

    def test_ph_threshold_alerts(self):
        reading = {"water_ph": 6.0}
        alerts = AlertEngine.analyze_readings_for_alerts(self.db, self.user.id, reading, {})
        self.assertEqual(len(alerts), 0)

        reading = {"water_ph": 5.2}
        alerts = AlertEngine.analyze_readings_for_alerts(self.db, self.user.id, reading, {})
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["severity"], "warning")
        self.assertEqual(alerts[0]["alert_type"], "water_ph")

        self.db.query(models.Alert).delete()
        self.db.commit()
        reading = {"water_ph": 4.5}
        alerts = AlertEngine.analyze_readings_for_alerts(self.db, self.user.id, reading, {})
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["severity"], "critical")

    def test_temperature_alerts(self):
        reading = {"temperature": 32.5}
        alerts = AlertEngine.analyze_readings_for_alerts(self.db, self.user.id, reading, {})
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["severity"], "critical")
        self.assertEqual(alerts[0]["alert_type"], "temperature")
