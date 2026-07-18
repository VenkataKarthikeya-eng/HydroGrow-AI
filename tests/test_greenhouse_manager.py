import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, User
from backend.services.farm_management.farm_manager import FarmManager
from backend.services.farm_management.greenhouse_manager import GreenhouseManager

class TestGreenhouseManager(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

        self.user = User(username="ghuser", email="gh@hydrogrow.ai", password_hash="pass")
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)

        self.farm = FarmManager.create_farm(self.db, self.user.id, "GH Test Farm")

    def tearDown(self):
        self.db.close()

    def test_create_and_list_greenhouses(self):
        gh_list = GreenhouseManager.list_greenhouses(self.db, self.farm.id)
        self.assertGreaterEqual(len(gh_list), 1)

        new_gh = GreenhouseManager.create_greenhouse(self.db, self.farm.id, "Zone 3 - Aeroponics")
        self.assertEqual(new_gh.name, "Zone 3 - Aeroponics")

if __name__ == "__main__":
    unittest.main()
