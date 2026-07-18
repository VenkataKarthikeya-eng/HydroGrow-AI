import unittest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.api.main import app
from backend.database.connection import engine, Base, SessionLocal
from backend.authentication import security, jwt_handler

class TestAuthSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)
        import os
        if os.path.exists("test_hydrogrow.db"):
            try:
                os.remove("test_hydrogrow.db")
            except Exception:
                pass

    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_password_hashing(self):
        password = "mysecretpassword"
        hashed = security.get_password_hash(password)
        self.assertNotEqual(password, hashed)
        self.assertTrue(security.verify_password(password, hashed))
        self.assertFalse(security.verify_password("wrongpassword", hashed))

    def test_jwt_token_handling(self):
        data = {"sub": "testgrower", "user_id": 99}
        token = jwt_handler.create_access_token(data)
        self.assertIsNotNone(token)
        
        decoded = jwt_handler.decode_token(token)
        self.assertEqual(decoded["sub"], "testgrower")
        self.assertEqual(decoded["user_id"], 99)

    def test_registration_and_login_api(self):
        # 1. Register new user
        reg_payload = {
            "username": "authgrower",
            "email": "authgrower@example.com",
            "password": "growerpassword"
        }
        response = self.client.post("/api/auth/register", json=reg_payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["username"], "authgrower")
        self.assertEqual(json_data["email"], "authgrower@example.com")
        self.assertIn("id", json_data)

        # 2. Register same username (should fail)
        dup_response = self.client.post("/api/auth/register", json=reg_payload)
        self.assertEqual(dup_response.status_code, 400)

        # 3. Login
        login_payload = {
            "username": "authgrower",
            "password": "growerpassword"
        }
        login_response = self.client.post("/api/auth/login", json=login_payload)
        self.assertEqual(login_response.status_code, 200)
        token_data = login_response.json()
        self.assertEqual(token_data["token_type"], "bearer")
        self.assertIn("access_token", token_data)

        # 4. Login with wrong password (should fail)
        wrong_payload = {
            "username": "authgrower",
            "password": "wrongpassword"
        }
        wrong_response = self.client.post("/api/auth/login", json=wrong_payload)
        self.assertEqual(wrong_response.status_code, 401)
