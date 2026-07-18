import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base
from backend.services.global_intelligence.strategy_engine import StrategyEngine

class TestStrategyEngine(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_generate_and_rank_strategies(self):
        plans = StrategyEngine.generate_strategy(self.db, farm_id=1)
        self.assertGreaterEqual(len(plans), 1)

        ranked = StrategyEngine.rank_strategies(plans)
        self.assertEqual(len(ranked), len(plans))

if __name__ == "__main__":
    unittest.main()
