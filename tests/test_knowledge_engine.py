import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base
from backend.services.agriculture_intelligence.knowledge_engine import KnowledgeEngine

class TestKnowledgeEngine(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_search_and_best_practices(self):
        articles = KnowledgeEngine.search_crop_knowledge(self.db, "EC", "Lettuce")
        self.assertIsInstance(articles, list)

        bp = KnowledgeEngine.get_best_practices("Lettuce")
        self.assertIn("optimal_ph", bp)

        guidelines = KnowledgeEngine.generate_crop_guidelines("Lettuce")
        self.assertIn("title", guidelines)

if __name__ == "__main__":
    unittest.main()
