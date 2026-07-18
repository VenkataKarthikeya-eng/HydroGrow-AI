import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base
from backend.mlops.training_scheduler import TrainingScheduler

class TestTrainingScheduler(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_check_retrain_needed(self):
        res = TrainingScheduler.check_retrain_needed(self.db)
        self.assertIn("retrain_recommended", res)
        self.assertIn("current_accuracy", res)

if __name__ == "__main__":
    unittest.main()
