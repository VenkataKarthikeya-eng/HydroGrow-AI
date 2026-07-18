import unittest
from backend.ml.preprocessing.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):

    def test_handle_missing_values(self):
        raw = {"air_temperature": 24.5, "co2": None}
        cleaned = DataProcessor.handle_missing_values(raw)
        self.assertEqual(cleaned["air_temperature"], 24.5)
        self.assertEqual(cleaned["co2"], 450.0)

    def test_generate_synthetic_agronomic_dataset(self):
        X, y = DataProcessor.generate_synthetic_agronomic_dataset(num_samples=50)
        self.assertEqual(X.shape[0], 50)
        self.assertEqual(X.shape[1], 11)
        self.assertEqual(len(y), 50)

if __name__ == "__main__":
    unittest.main()
