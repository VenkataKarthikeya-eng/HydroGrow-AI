import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, User
from backend.services.farm_management.farm_manager import FarmManager
from backend.services.farm_management.permission_manager import PermissionManager

class TestPermissions(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

        self.owner = User(username="owneruser", email="owner@hydrogrow.ai", password_hash="pass")
        self.db.add(self.owner)
        self.db.commit()
        self.db.refresh(self.owner)

        self.farm = FarmManager.create_farm(self.db, self.owner.id, "Permission Test Farm")

    def tearDown(self):
        self.db.close()

    def test_owner_permissions(self):
        is_owner = PermissionManager.has_permission(self.db, self.farm.id, self.owner.id, "OWNER")
        self.assertTrue(is_owner)
        is_manager = PermissionManager.has_permission(self.db, self.farm.id, self.owner.id, "MANAGER")
        self.assertTrue(is_manager)

if __name__ == "__main__":
    unittest.main()
