import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, User
from backend.cloud.device_manager import DeviceManager

class TestDeviceManager(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

        self.user = User(
            username="devuser",
            email="dev_test@hydrogrow.ai",
            password_hash="mockpass"
        )
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)

    def tearDown(self):
        self.db.close()

    def test_register_and_authenticate_device(self):
        res = DeviceManager.register_device(
            db=self.db,
            user_id=self.user.id,
            device_id="ESP32_TEST_01",
            device_type="ESP32"
        )
        self.assertEqual(res["device_id"], "ESP32_TEST_01")
        self.assertTrue(res["api_key"].startswith("hg_key_"))

        valid = DeviceManager.authenticate_device(self.db, "ESP32_TEST_01", res["api_key"])
        self.assertTrue(valid)

if __name__ == "__main__":
    unittest.main()
