import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, User
from backend.services.farm_management.farm_manager import FarmManager
from backend.services.farm_management.permission_manager import PermissionManager

class TestMultiTenantSecurity(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

        self.user_a = User(username="usera", email="usera@hydrogrow.ai", password_hash="pass")
        self.user_b = User(username="userb", email="userb@hydrogrow.ai", password_hash="pass")
        self.db.add(self.user_a)
        self.db.add(self.user_b)
        self.db.commit()
        self.db.refresh(self.user_a)
        self.db.refresh(self.user_b)

        self.farm_a = FarmManager.create_farm(self.db, self.user_a.id, "User A Isolated Farm")

    def tearDown(self):
        self.db.close()

    def test_tenant_data_isolation(self):
        # User B tries to fetch User A's farm
        farm = FarmManager.get_farm_by_id(self.db, self.farm_a.id, self.user_b.id)
        self.assertIsNone(farm)

        # User B tries to delete User A's farm
        deleted = FarmManager.delete_farm(self.db, self.farm_a.id, self.user_b.id)
        self.assertFalse(deleted)

        # Permission check for User B on User A's farm
        has_perm = PermissionManager.has_permission(self.db, self.farm_a.id, self.user_b.id, "VIEWER")
        self.assertFalse(has_perm)

if __name__ == "__main__":
    unittest.main()
