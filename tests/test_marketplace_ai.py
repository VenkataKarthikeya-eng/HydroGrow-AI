import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.api.main import app
from backend.database.connection import get_db
from backend.database.models import Base

class TestMarketplaceAI(unittest.TestCase):

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

        app.dependency_overrides[get_db] = override_get_db
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()

    def test_marketplace_ai_endpoints(self):
        res_t = self.client.get("/api/marketplace/trending-products")
        self.assertEqual(res_t.status_code, 200)

        res_r = self.client.get("/api/marketplace/recommendations")
        self.assertEqual(res_r.status_code, 200)

if __name__ == "__main__":
    unittest.main()
