import unittest
from fastapi.testclient import TestClient
from backend.api.main import app

class TestHealthEndpoint(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")
        self.assertEqual(data["version"], "1.0")

if __name__ == "__main__":
    unittest.main()
