import unittest
import json
import os
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas
from backend.authentication import jwt_handler

class TestStreamingChatAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)
        
        # Create test grower for authenticated stream checks
        cls.db = SessionLocal()
        user_schema = schemas.UserCreate(
            username="streamgrower",
            email="streamgrower@example.com",
            password="growerpassword"
        )
        cls.user = crud.create_user(cls.db, user=user_schema, password_hash="hashed_password_val")
        cls.db.commit()
        
        # Generate token
        cls.token = jwt_handler.create_access_token({"sub": cls.user.username, "user_id": cls.user.id})
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("test_hydrogrow.db"):
            try:
                os.remove("test_hydrogrow.db")
            except Exception:
                pass

    def test_streaming_chat_anonymous(self):
        payload = {
            "message": "Why is my prediction low?",
            "conversation_history": [],
            "context": {
                "user_inputs": {
                    "water_ph": 4.5,
                    "water_ec": 2.0,
                    "co2": 400.0,
                    "air_temperature": 22.0,
                    "humidity": 60.0
                }
            }
        }
        # Run request anonymously (without headers)
        response = self.client.post("/api/chat/stream", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "text/event-stream; charset=utf-8")

        # Parse text chunks
        chunks = []
        for line in response.iter_lines():
            if line:
                chunk_data = json.loads(line)
                self.assertIn("chunk", chunk_data)
                self.assertIn("sources", chunk_data)
                self.assertIn("intent", chunk_data)
                chunks.append(chunk_data["chunk"])

        full_text = "".join(chunks)
        self.assertGreater(len(full_text), 0)

    def test_streaming_chat_authenticated(self):
        # Create conversation thread
        conv = crud.create_conversation(self.db, user_id=self.user.id, title="Stream test")
        
        payload = {
            "message": "Explain what high water pH (7.2) does to lettuce",
            "conversation_history": [],
            "context": {},
            "conversation_id": conv.id
        }
        # Run authenticated
        response = self.client.post("/api/chat/stream", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        chunks = []
        for line in response.iter_lines():
            if line:
                chunk_data = json.loads(line)
                self.assertEqual(chunk_data["conversation_id"], conv.id)
                chunks.append(chunk_data["chunk"])

        full_text = "".join(chunks)
        self.assertIn("Insight", full_text)
        self.assertIn("Analysis", full_text)
