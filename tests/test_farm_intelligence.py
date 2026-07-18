import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base
from backend.services.global_intelligence.farm_intelligence_engine import FarmIntelligenceEngine

class TestFarmIntelligence(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_calculate_farm_score_and_insights(self):
        score_data = FarmIntelligenceEngine.calculate_farm_score(self.db, farm_id=1)
        self.assertEqual(score_data["farm_id"], 1)
        self.assertGreater(score_data["overall_score"], 0)

        insights = FarmIntelligenceEngine.generate_farm_insights(self.db, farm_id=1)
        self.assertIsInstance(insights, list)

        bottlenecks = FarmIntelligenceEngine.detect_productivity_bottlenecks(self.db, farm_id=1)
        self.assertIsInstance(bottlenecks, list)

if __name__ == "__main__":
    unittest.main()
