import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base
from backend.services.agriculture_intelligence.expert_matching import ExpertMatching

class TestExpertMatching(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_expert_matching(self):
        experts = ExpertMatching.match_experts(self.db, "Pathology", "Lettuce")
        self.assertGreaterEqual(len(experts), 1)

if __name__ == "__main__":
    unittest.main()
