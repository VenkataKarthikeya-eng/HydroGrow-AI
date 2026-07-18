import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.api.main import app
from backend.database.connection import get_db
from backend.database.models import Base
from backend.authentication.jwt_handler import get_optional_current_user

class TestMLRoutes(unittest.TestCase):

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
            username = "mlrouteuser"
            email = "ml_route@hydrogrow.ai"

        def override_get_user():
            return MockUser()

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_optional_current_user] = override_get_user
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()

    def test_list_models_endpoint(self):
        res = self.client.get("/api/ml/models")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_performance_endpoint(self):
        res = self.client.get("/api/ml/performance")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("active_models_count", data)

    def test_datasets_endpoint(self):
        res = self.client.get("/api/ml/datasets")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

if __name__ == "__main__":
    unittest.main()
