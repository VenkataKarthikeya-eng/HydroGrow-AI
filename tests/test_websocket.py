import unittest
import os
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.authentication import jwt_handler

class TestWebSocket(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)
        cls.db = SessionLocal()

        # Clear existing users
        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="wsgrower",
            email="ws@example.com",
            password="growerpassword"
        )
        cls.user = crud.create_user(cls.db, user=user_schema, password_hash="hashed")
        cls.db.commit()

        cls.token = jwt_handler.create_access_token({"sub": cls.user.username, "user_id": cls.user.id})

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("test_hydrogrow.db"):
            try:
                os.remove("test_hydrogrow.db")
            except Exception:
                pass

    def test_websocket_unauthorized_rejection(self):
        with self.assertRaises(Exception):
            with self.client.websocket_connect("/ws/iot/live") as websocket:
                pass

        with self.assertRaises(Exception):
            with self.client.websocket_connect("/ws/iot/live?token=invalidtoken") as websocket:
                pass

    def test_websocket_authorized_connection(self):
        with self.client.websocket_connect(f"/ws/iot/live?token={self.token}") as websocket:
            pass
