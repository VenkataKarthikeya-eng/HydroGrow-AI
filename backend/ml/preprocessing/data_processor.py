import numpy as np

DEFAULT_PREDICTOR_VALUES = {
    "air_temperature": 22.0,
    "humidity": 60.0,
    "co2": 450.0,
    "water_ph": 6.2,
    "water_ec": 2.0,
    "water_temperature": 23.0,
    "nutrient_solution": 400.0,
    "water_consumption": 170.0,
    "seedling_height": 12.0,
    "seedling_weight": 4.0,
    "root_length": 7.0
}

FEATURE_ORDER = [
    "air_temperature", "humidity", "co2", "water_ph", "water_ec",
    "water_temperature", "nutrient_solution", "water_consumption",
    "seedling_height", "seedling_weight", "root_length"
]

class DataProcessor:
    """
    Data Cleaning, Missing Value Imputation, and Feature Normalization Pipeline.
    """

    @staticmethod
    def handle_missing_values(raw_inputs: dict) -> dict:
        processed = {}
        for feat in FEATURE_ORDER:
            val = raw_inputs.get(feat)
            if val is None or (isinstance(val, (int, float)) and np.isnan(val)):
                processed[feat] = DEFAULT_PREDICTOR_VALUES[feat]
            else:
                processed[feat] = float(val)
        return processed

    @staticmethod
    def normalize_features(features_dict: dict) -> list:
        cleaned = DataProcessor.handle_missing_values(features_dict)
        return [cleaned[feat] for feat in FEATURE_ORDER]

    @staticmethod
    def generate_synthetic_agronomic_dataset(num_samples: int = 500) -> tuple:
        np.random.seed(42)
        X = []
        y = []
        for _ in range(num_samples):
            temp = np.random.uniform(16.0, 32.0)
            hum = np.random.uniform(40.0, 85.0)
            co2 = np.random.uniform(300.0, 800.0)
            ph = np.random.uniform(4.5, 7.5)
            ec = np.random.uniform(1.0, 3.0)
            wtemp = np.random.uniform(18.0, 28.0)
            nutr = np.random.uniform(200.0, 600.0)
            wcons = np.random.uniform(100.0, 250.0)
            s_h = np.random.uniform(5.0, 18.0)
            s_w = np.random.uniform(1.5, 8.0)
            r_l = np.random.uniform(3.0, 12.0)

            # Realistic lettuce fresh weight synthesis with stress penalties
            base_weight = 250.0 + (s_w * 15.0) + (co2 * 0.1) + (nutr * 0.05)
            # Penalties
            if temp > 28.0 or temp < 18.0:
                base_weight -= 40.0
            if ph < 5.5 or ph > 6.8:
                base_weight -= 50.0
            if ec < 1.4 or ec > 2.5:
                base_weight -= 35.0

            noise = np.random.normal(0, 10)
            fresh_weight = max(100.0, round(base_weight + noise, 2))

            row = [temp, hum, co2, ph, ec, wtemp, nutr, wcons, s_h, s_w, r_l]
            X.append(row)
            y.append(fresh_weight)

        return np.array(X), np.array(y)
