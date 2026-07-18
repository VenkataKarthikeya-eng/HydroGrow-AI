import unittest
import os
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.services.iot.sensor_manager import SensorManager

class TestSensorManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()

        # Clear existing users
        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="iotgrower",
            email="iotgrower@example.com",
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

    def test_register_and_get_devices(self):
        devices = SensorManager.get_user_devices(self.db, self.user.id)
        self.assertEqual(len(devices), 0)

        dev = SensorManager.register_sensor(
            db=self.db,
            user_id=self.user.id,
            device_name="Test Sensor Tank",
            location="Zone B"
        )
        self.assertEqual(dev.device_name, "Test Sensor Tank")
        self.assertEqual(dev.location, "Zone B")

        devices = SensorManager.get_user_devices(self.db, self.user.id)
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0].id, dev.id)

    def test_save_and_retrieve_readings(self):
        dev = SensorManager.register_sensor(
            db=self.db,
            user_id=self.user.id,
            device_name="Tank Sensor"
        )
        
        reading = SensorManager.save_sensor_reading(
            db=self.db,
            device_id=dev.id,
            temperature=24.5,
            humidity=65.0,
            water_ph=6.0,
            water_ec=1.8,
            water_temperature=21.0,
            co2=450.0,
            nutrient_level=95.0
        )
        self.assertEqual(reading.temperature, 24.5)
        self.assertEqual(reading.water_ph, 6.0)

        latest = SensorManager.get_latest_reading(self.db, self.user.id, dev.id)
        self.assertIsNotNone(latest)
        self.assertEqual(latest.water_ec, 1.8)

        hist = SensorManager.get_readings_history(self.db, self.user.id, dev.id)
        self.assertEqual(len(hist), 1)
