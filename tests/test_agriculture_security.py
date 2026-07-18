import unittest
from fastapi.testclient import TestClient
from backend.api.main import app

class TestAgricultureSecurity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_unauthenticated_protected_routes(self):
        # Create product requires authentication
        res = self.client.post("/api/marketplace/products", json={"product_name": "Unauth Product", "price": 10})
        self.assertEqual(res.status_code, 401)

        # Create post requires authentication
        res = self.client.post("/api/community/1/post", json={"content": "Unauth Post"})
        self.assertEqual(res.status_code, 401)

        # Request expert consultation requires authentication
        res = self.client.post("/api/experts/request", json={"expert_id": 1, "issue_description": "Root burn"})
        self.assertEqual(res.status_code, 401)

if __name__ == "__main__":
    unittest.main()
