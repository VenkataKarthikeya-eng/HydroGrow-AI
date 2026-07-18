import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.api.main import app
from backend.database.connection import get_db
from backend.database.models import Base
from backend.authentication.jwt_handler import get_optional_current_user

class TestMarketplaceRoutes(unittest.TestCase):

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
            username = "selleruser"
            email = "seller@hydrogrow.ai"

        def override_get_user():
            return MockUser()

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_optional_current_user] = override_get_user
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()

    def test_list_and_create_product(self):
        res = self.client.get("/api/marketplace/products")
        self.assertEqual(res.status_code, 200)

        create_res = self.client.post("/api/marketplace/products", json={
            "product_name": "Test Hydro Nutrients 5L",
            "price": 29.99,
            "category": "Nutrients & Concentrates"
        })
        self.assertEqual(create_res.status_code, 200)

if __name__ == "__main__":
    unittest.main()
