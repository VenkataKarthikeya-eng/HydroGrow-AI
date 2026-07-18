import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, User
from backend.services.farm_management.farm_manager import FarmManager
from backend.services.farm_management.subscription_manager import SubscriptionManager

class TestSubscription(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

        self.user = User(username="subuser", email="sub@hydrogrow.ai", password_hash="pass")
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)

        self.farm = FarmManager.create_farm(self.db, self.user.id, "Sub Test Farm")

    def tearDown(self):
        self.db.close()

    def test_get_farm_subscription(self):
        sub_info = SubscriptionManager.get_farm_subscription(self.db, self.farm.id)
        self.assertEqual(sub_info["plan"], "FREE")
        self.assertEqual(sub_info["max_devices"], 3)

if __name__ == "__main__":
    unittest.main()
