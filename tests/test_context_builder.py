import unittest
import os
from backend.services.intelligence.intent_classifier import IntentClassifier
from backend.rag.query_processor import QueryProcessor
from backend.rag.document_ranker import DocumentRanker
from backend.services.intelligence.context_builder import ContextBuilder
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas

class TestContextAndRAGUpgrades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()

        # Create test grower for prediction context check
        user_schema = schemas.UserCreate(
            username="contextgrower",
            email="contextgrower@example.com",
            password="growerpassword"
        )
        cls.user = crud.create_user(cls.db, user=user_schema, password_hash="hashed")
        cls.db.commit()

        # Save a mock prediction log
        crud.create_prediction(
            db=cls.db,
            user_id=cls.user.id,
            input_parameters={"water_ph": 6.2, "co2": 450.0},
            predicted_weight=350.5,
            growth_category="Excellent"
        )

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("test_hydrogrow.db"):
            try:
                os.remove("test_hydrogrow.db")
            except Exception:
                pass

    def test_intent_classification(self):
        # yields disease intent
        intent_disease = IntentClassifier.classify_intent("How do I cure root rot", "How do I cure root rot")
        self.assertEqual(intent_disease, "disease_diagnosis")

        # yields prediction comparison analysis intent
        intent_compare = IntentClassifier.classify_intent("Why is my prediction smaller than last week?", "Why is my prediction smaller than last week?")
        self.assertEqual(intent_compare, "previous_prediction_analysis")

        # yields general hydroponics intent
        intent_gen = IntentClassifier.classify_intent("how to construct a nft channel system", "how to construct a nft channel system")
        self.assertEqual(intent_gen, "general_hydroponics")

    def test_query_expansion(self):
        expanded = QueryProcessor.expand_query("root rot", "disease_diagnosis")
        self.assertIn("treatment", expanded)
        self.assertIn("root rot", expanded)
        self.assertIn("symptom", expanded)

    def test_document_ranking(self):
        docs = [
            {"content": "low match", "score": 0.05},
            {"content": "high match", "score": 0.99},
            {"content": "mid match", "score": 0.25}
        ]
        # Check sort order
        sorted_docs = DocumentRanker.rank_documents(docs)
        self.assertEqual(sorted_docs[0]["content"], "high match")
        self.assertEqual(sorted_docs[2]["content"], "low match")

        # Check filter
        filtered_docs = DocumentRanker.filter_relevant_context(docs, min_threshold=0.1)
        self.assertEqual(len(filtered_docs), 2)

    def test_context_builder(self):
        # 1. Build profile context
        profile = ContextBuilder.build_user_context(self.user.id, self.db)
        self.assertTrue(profile["authenticated"])
        self.assertEqual(profile["username"], "contextgrower")

        # 2. Build prediction history context
        pred_context = ContextBuilder.build_prediction_context(self.user.id, self.db)
        self.assertEqual(pred_context["predicted_weight"], 350.5)
        self.assertEqual(pred_context["growth_category"], "Excellent")
        self.assertEqual(pred_context["input_parameters"]["co2"], 450.0)
