import unittest
import os
import sys
from sqlalchemy.orm import Session
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.services.intelligence.conversation_manager import ConversationManager
from backend.services.intelligence.context_builder import ContextBuilder

class TestAIMemoryUpgrade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()

        # Create test user
        user_schema = schemas.UserCreate(
            username="memorygrower",
            email="memorygrower@example.com",
            password="growerpassword"
        )
        cls.user = crud.create_user(cls.db, user=user_schema, password_hash="hashed_password_val")
        cls.db.commit()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("test_hydrogrow.db"):
            try:
                os.remove("test_hydrogrow.db")
            except Exception:
                pass

    def test_auto_title_generation(self):
        # Match pH queries
        title_ph = ConversationManager.generate_conversation_title("why is water pH high?")
        self.assertEqual(title_ph, "Water pH Adjustment")

        # Match root rot queries
        title_rot = ConversationManager.generate_conversation_title("how to prevent root rot")
        self.assertEqual(title_rot, "Pythium Root Rot Diagnosis")

        # Fallback text
        title_fallback = ConversationManager.generate_conversation_title("what is deep water culture")
        self.assertEqual(title_fallback, "What Is Deep Water...")

    def test_conversation_metadata_and_auto_title_update(self):
        # Create initial conversation thread
        conv = crud.create_conversation(self.db, user_id=self.user.id, title="New grow room query")
        self.assertEqual(conv.title, "New grow room query")

        # Create first message
        crud.create_message(self.db, conversation_id=conv.id, role="user", content="How do I cure tipburn?")
        
        # Trigger metadata update
        updated_conv = ConversationManager.update_conversation_metadata(
            self.db, 
            conversation_id=conv.id, 
            new_message_content="How do I cure tipburn?"
        )
        self.assertIsNotNone(updated_conv)
        self.assertEqual(updated_conv.message_count, 1)
        self.assertEqual(updated_conv.title, "Tipburn Deficiency Issues")
