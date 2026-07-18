import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.api.main import app
from backend.database.connection import get_db
from backend.database.models import Base
from backend.authentication.jwt_handler import get_optional_current_user
from backend.services.farm_management.farm_manager import FarmManager

class TestIntelligenceRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )
        cls.TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        Base.metadata.create_all(bind=cls.engine)

        def override_get_db():
            db = cls.TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()

        class MockUser:
            id = 1
            username = "inteluser"
            email = "intel@hydrogrow.ai"

        def override_get_user():
            return MockUser()

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_optional_current_user] = override_get_user
        cls.client = TestClient(app)

        # Seed farm for user
        db = cls.TestingSessionLocal()
        cls.farm = FarmManager.create_farm(db, owner_id=1, farm_name="Intel Farm 1")
        db.close()

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()

    def test_intelligence_endpoints(self):
        res = self.client.get(f"/api/intelligence/farm-score/{self.farm.id}")
        self.assertEqual(res.status_code, 200)

        res_p = self.client.get(f"/api/intelligence/profit-analysis/{self.farm.id}")
        self.assertEqual(res_p.status_code, 200)

        res_m = self.client.get("/api/intelligence/market-trends")
        self.assertEqual(res_m.status_code, 200)

        res_s = self.client.get(f"/api/intelligence/strategy/{self.farm.id}")
        self.assertEqual(res_s.status_code, 200)

if __name__ == "__main__":
    unittest.main()
