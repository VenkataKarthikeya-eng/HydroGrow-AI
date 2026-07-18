import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.api.main import app
from backend.database.connection import get_db
from backend.database.models import Base
from backend.authentication.jwt_handler import get_optional_current_user

class TestFarmRoutes(unittest.TestCase):

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
            username = "farmrouteuser"
            email = "farm_route@hydrogrow.ai"

        def override_get_user():
            return MockUser()

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_optional_current_user] = override_get_user
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()

    def test_list_farms_endpoint(self):
        res = self.client.get("/api/farms")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_create_farm_endpoint(self):
        res = self.client.post("/api/farms/create", json={"farm_name": "API Test Facility C"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["farm_name"], "API Test Facility C")

    def test_marketplace_templates_endpoint(self):
        res = self.client.get("/api/marketplace/templates")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

if __name__ == "__main__":
    unittest.main()
