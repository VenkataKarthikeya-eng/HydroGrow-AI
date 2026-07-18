import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, User
from backend.services.farm_management.farm_manager import FarmManager

class TestFarmManager(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

        self.user = User(
            username="farmuser",
            email="farm_owner@hydrogrow.ai",
            password_hash="mockpass"
        )
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)

    def tearDown(self):
        self.db.close()

    def test_create_and_get_user_farms(self):
        farms = FarmManager.get_user_farms(self.db, self.user.id)
        self.assertEqual(len(farms), 1) # Auto-provisioned default farm
        self.assertEqual(farms[0].farm_name, "My Smart Farm")

        new_farm = FarmManager.create_farm(
            db=self.db,
            owner_id=self.user.id,
            farm_name="Greenhouse Facility B"
        )
        self.assertEqual(new_farm.farm_name, "Greenhouse Facility B")

        all_farms = FarmManager.get_user_farms(self.db, self.user.id)
        self.assertEqual(len(all_farms), 2)

if __name__ == "__main__":
    unittest.main()
