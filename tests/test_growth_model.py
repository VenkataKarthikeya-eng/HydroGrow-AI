import unittest
from backend.ml.preprocessing.data_processor import DataProcessor
from backend.ml.models.growth_model import GrowthModel

class TestGrowthModel(unittest.TestCase):

    def test_train_and_predict_growth(self):
        X, y = DataProcessor.generate_synthetic_agronomic_dataset(num_samples=100)
        gm = GrowthModel()
        score = gm.train_growth_model(X, y)
        self.assertGreaterEqual(score, 0.5)

        features = {
            "air_temperature": 22.0, "humidity": 60.0, "co2": 450.0,
            "water_ph": 6.2, "water_ec": 2.0, "water_temperature": 23.0,
            "nutrient_solution": 400.0, "water_consumption": 170.0,
            "seedling_height": 12.0, "seedling_weight": 4.0, "root_length": 7.0
        }
        res = gm.predict_growth(features)
        self.assertIn("fresh_weight", res)
        self.assertIn("confidence_score", res)
        self.assertTrue(res["is_ml_model"])

if __name__ == "__main__":
    unittest.main()
