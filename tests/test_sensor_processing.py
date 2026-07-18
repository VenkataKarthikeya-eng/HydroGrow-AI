import unittest
import os
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.services.iot.sensor_manager import SensorManager
from backend.services.iot.data_processor import DataProcessor

class TestSensorProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()

        # Clear existing users
        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="processinggrower",
            email="proc@example.com",
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
        self.db.query(models.SensorReading).delete()
        self.db.query(models.SensorDevice).delete()
        self.db.commit()

    def test_range_validations(self):
        valid_reading = {
            "temperature": 24.5,
            "humidity": 65.0,
            "water_ph": 6.1,
            "water_ec": 1.8,
            "co2": 500.0
        }
        self.assertTrue(DataProcessor.validate_reading(valid_reading))

        invalid_temp = valid_reading.copy()
        invalid_temp["temperature"] = 52.0
        self.assertFalse(DataProcessor.validate_reading(invalid_temp))

        invalid_ph = valid_reading.copy()
        invalid_ph["water_ph"] = -0.5
        self.assertFalse(DataProcessor.validate_reading(invalid_ph))

        invalid_ec = valid_reading.copy()
        invalid_ec["water_ec"] = 11.2
        self.assertFalse(DataProcessor.validate_reading(invalid_ec))

    def test_moving_averages_calculation(self):
        dev = SensorManager.register_sensor(
            db=self.db,
            user_id=self.user.id,
            device_name="Average Sensor"
        )

        SensorManager.save_sensor_reading(self.db, dev.id, temperature=20.0, humidity=50.0, water_ph=6.0, water_ec=1.5, water_temperature=20.0, co2=400.0)
        SensorManager.save_sensor_reading(self.db, dev.id, temperature=22.0, humidity=60.0, water_ph=6.2, water_ec=1.7, water_temperature=22.0, co2=420.0)

        current = {
            "temperature": 24.0,
            "humidity": 70.0,
            "water_ph": 6.4,
            "water_ec": 1.9,
            "water_temperature": 24.0,
            "co2": 440.0,
            "nutrient_level": 90.0
        }

        averages = DataProcessor.calculate_moving_averages(self.db, self.user.id, dev.id, current)
        self.assertEqual(averages["temperature"], 22.0)
        self.assertEqual(averages["water_ph"], 6.2)
        self.assertEqual(averages["water_ec"], 1.7)
