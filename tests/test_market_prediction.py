import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base
from backend.services.global_intelligence.market_prediction_engine import MarketPredictionEngine

class TestMarketPrediction(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_market_predictions(self):
        pred = MarketPredictionEngine.predict_crop_price(self.db, "Butterhead Lettuce")
        self.assertEqual(pred["crop_name"], "Butterhead Lettuce")

        report = MarketPredictionEngine.generate_market_report(self.db)
        self.assertIsInstance(report, list)

if __name__ == "__main__":
    unittest.main()
