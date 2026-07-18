import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base
from backend.mlops.model_monitor import ModelMonitor

class TestMLOpsMonitor(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_get_monitoring_metrics(self):
        metrics = ModelMonitor.get_monitoring_metrics(self.db)
        self.assertIn("total_inference_calls", metrics)
        self.assertIn("average_confidence", metrics)
        self.assertIn("average_latency_ms", metrics)

if __name__ == "__main__":
    unittest.main()
