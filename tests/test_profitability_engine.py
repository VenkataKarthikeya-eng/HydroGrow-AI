import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base
from backend.services.global_intelligence.profitability_engine import ProfitabilityEngine

class TestProfitabilityEngine(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_profitability_calculations(self):
        profit = ProfitabilityEngine.calculate_crop_profit(self.db, farm_id=1)
        self.assertEqual(profit["farm_id"], 1)
        self.assertGreater(profit["profit_margin"], 0)

        comp = ProfitabilityEngine.compare_crop_profitability(self.db, farm_id=1)
        self.assertIsInstance(comp, list)

if __name__ == "__main__":
    unittest.main()
