import unittest
from fastapi.testclient import TestClient
from backend.api.main import app

class TestSecurityMiddleware(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_security_headers_present(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("x-frame-options"), "DENY")
        self.assertEqual(res.headers.get("x-content-type-options"), "nosniff")

if __name__ == "__main__":
    unittest.main()
