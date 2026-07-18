import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, User
from backend.ml.inference.ml_engine import MLEngine

class TestMLInference(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

        self.user = User(
            username="mluser",
            email="ml_test@hydrogrow.ai",
            password_hash="hashedpass"
        )
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)

    def tearDown(self):
        self.db.close()

    def test_run_growth_prediction(self):
        inputs = {
            "air_temperature": 22.0, "humidity": 60.0, "co2": 450.0,
            "water_ph": 6.2, "water_ec": 2.0, "water_temperature": 23.0,
            "nutrient_solution": 400.0, "water_consumption": 170.0,
            "seedling_height": 12.0, "seedling_weight": 4.0, "root_length": 7.0
        }
        res = MLEngine.run_growth_prediction(self.db, self.user.id, inputs)
        self.assertIn("fresh_weight", res)
        self.assertIn("inference_time", res)

if __name__ == "__main__":
    unittest.main()
