import unittest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.api.main import app
from backend.database.connection import engine, Base, SessionLocal
from backend.authentication import jwt_handler

class TestHistoryAndPersistence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

        # Create a test user and generate token
        db = SessionLocal()
        from backend.database import crud, schemas
        user_schema = schemas.UserCreate(
            username="historyuser",
            email="historyuser@example.com",
            password="password"
        )
        db_user = crud.create_user(db, user=user_schema, password_hash="hash")
        cls.token = jwt_handler.create_access_token({"sub": db_user.username, "user_id": db_user.id})
        cls.headers = {"Authorization": f"Bearer {cls.token}"}
        db.close()

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)
        import os
        if os.path.exists("test_hydrogrow.db"):
            try:
                os.remove("test_hydrogrow.db")
            except Exception:
                pass

    def test_predict_saves_to_history(self):
        # 1. Run prediction anonymously (no headers)
        pred_payload = {
            "air_temperature": 22.0,
            "humidity": 60.0,
            "co2": 450.0,
            "water_ph": 6.2,
            "water_ec": 2.0,
            "water_temperature": 23.0,
            "nutrient_solution": 400.0,
            "water_consumption": 170.0,
            "seedling_height": 12.0,
            "seedling_weight": 4.0,
            "root_length": 7.0
        }
        anon_response = self.client.post("/api/predict", json=pred_payload)
        self.assertEqual(anon_response.status_code, 200)

        # Check prediction history for user is still empty
        history_response = self.client.get("/api/history/predictions", headers=self.headers)
        self.assertEqual(len(history_response.json()), 0)

        # 2. Run prediction authenticated
        auth_response = self.client.post("/api/predict", json=pred_payload, headers=self.headers)
        self.assertEqual(auth_response.status_code, 200)

        # Check prediction history for user now has 1 record
        history_response2 = self.client.get("/api/history/predictions", headers=self.headers)
        self.assertEqual(len(history_response2.json()), 1)
        record = history_response2.json()[0]
        self.assertEqual(record["growth_category"], auth_response.json()["prediction"]["growth_category"])

    def test_chat_saves_to_conversations(self):
        # 1. Create a conversation thread
        conv_payload = {"title": "Lettuce Problems"}
        conv_response = self.client.post("/api/history/chats", json=conv_payload, headers=self.headers)
        self.assertEqual(conv_response.status_code, 200)
        conv_id = conv_response.json()["id"]

        # 2. Send message inside the thread
        chat_payload = {
            "message": "Why is my prediction low?",
            "conversation_history": [],
            "context": {},
            "conversation_id": conv_id
        }
        chat_response = self.client.post("/api/chat", json=chat_payload, headers=self.headers)
        self.assertEqual(chat_response.status_code, 200)

        # 3. Retrieve messages
        messages_response = self.client.get(f"/api/history/chats/{conv_id}", headers=self.headers)
        self.assertEqual(messages_response.status_code, 200)
        messages = messages_response.json()
        self.assertEqual(len(messages), 2) # User message + AI response
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[0]["content"], "Why is my prediction low?")
        self.assertEqual(messages[1]["role"], "assistant")
        self.assertIn("response", chat_response.json())
        self.assertEqual(messages[1]["content"], chat_response.json()["response"])
