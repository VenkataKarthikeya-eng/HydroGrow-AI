import os
import sys
import io
from pathlib import Path
from PIL import Image
import numpy as np

try:
    import tensorflow as tf
    HAS_TF = True
except ImportError:
    tf = None
    HAS_TF = False

try:
    import os as _os
    _os.environ['KERAS_BACKEND'] = 'torch'
    import keras
    HAS_KERAS = True
except Exception:
    keras = None
    HAS_KERAS = False

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

candidates = [
    PROJECT_ROOT / "ml_models" / "nutrient_model.pth",
    PROJECT_ROOT.parent / "backend" / "ml_models" / "nutrient_model.pth",
    PROJECT_ROOT.parent / "ml" / "models" / "nutrient_model.pth",
    PROJECT_ROOT / "ml_models" / "nutrient_model.keras",
    PROJECT_ROOT.parent / "ml" / "models" / "nutrient_model.keras",
]
MODEL_PATH = candidates[0]
for cand in candidates:
    if cand.exists():
        MODEL_PATH = cand
        break

CLASS_NAMES = ['healthy', 'nitrogen_deficiency', 'phosphorus_deficiency', 'potassium_deficiency']

CONDITION_DISPLAY_NAMES = {
    'healthy': "Healthy",
    'nitrogen_deficiency': "Nitrogen Deficiency",
    'phosphorus_deficiency': "Phosphorus Deficiency",
    'potassium_deficiency': "Potassium Deficiency"
}

RECOMMENDATIONS = {
    'healthy': "Plant nutrients are balanced. Continue current schedule.",
    'nitrogen_deficiency': "Increase nitrogen concentration and monitor chlorosis.",
    'phosphorus_deficiency': "Improve phosphorus availability for root and energy development.",
    'potassium_deficiency': "Increase potassium supply for plant strength and stress tolerance."
}

class NutrientPredictionService:
    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = Path(model_path)
        self.model = None
        self._load_model()

    def _load_model(self):
        if self.model_path.exists():
            try:
                if HAS_KERAS:
                    self.model = keras.models.load_model(str(self.model_path), compile=False)
                    print(f"[Model Loader] Nutrient Model loaded successfully from '{self.model_path}' [OK]")
                elif HAS_TF:
                    self.model = tf.keras.models.load_model(str(self.model_path), compile=False)
                    print(f"[Model Loader] Nutrient Model loaded successfully from '{self.model_path}' [OK]")
                else:
                    print(f"[Model Loader] Nutrient Model loading FAILED: Neither Keras nor TensorFlow available to load '{self.model_path}'. Fallback mode active.")
                    self.model = None
            except Exception as e:
                print(f"[Model Loader] Nutrient Model loading FAILED from '{self.model_path}': {e}. Fallback mode active.")
                self.model = None
        else:
            print(f"[Model Loader] Nutrient Model file NOT FOUND at '{self.model_path}'. Fallback mode active.")
            self.model = None

    def warm_up(self):
        """Warm up TensorFlow model execution graph during startup."""
        if self.model is not None:
            try:
                dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
                _ = self.model(dummy, training=False) if callable(self.model) else self.model.predict(dummy)
            except Exception as e:
                print(f"[NutrientPrediction] Warm-up warning: {e}")

    def predict_image(self, image_input, arr_input: np.ndarray = None) -> dict:
        res, _ = self.predict_image_fast(image_input, arr_input)
        return res

    def predict_image_fast(self, image_input, arr_input: np.ndarray = None) -> tuple[dict, float]:
        import time
        t0 = time.perf_counter()

        if isinstance(image_input, bytes):
            try:
                image = Image.open(io.BytesIO(image_input)).convert('RGB')
            except Exception as e:
                raise ValueError(f"Invalid image content: {str(e)}")
        elif isinstance(image_input, Image.Image):
            image = image_input
        else:
            image = None

        prediction_source = "ml_model"

        if self.model is not None:
            try:
                if arr_input is not None:
                    arr = arr_input
                elif image is not None:
                    img_resized = image.resize((224, 224))
                    arr = np.array(img_resized, dtype=np.float32) / 255.0
                    arr = np.expand_dims(arr, axis=0)
                else:
                    arr = np.zeros((1, 224, 224, 3), dtype=np.float32)

                preds = self.model(arr, training=False) if callable(self.model) else self.model.predict(arr)
                probs = preds[0].numpy() if hasattr(preds[0], 'numpy') else np.array(preds[0])
                pred_idx = int(np.argmax(probs))
                confidence = float(probs[pred_idx])
                if confidence < 0 or confidence > 1:
                    exp = np.exp(probs - np.max(probs))
                    p = exp / np.sum(exp)
                    confidence = float(p[pred_idx])
                raw_class = CLASS_NAMES[pred_idx]
            except Exception as ex:
                print(f"[NutrientPrediction] Model inference failed: {ex}. Using computer vision fallback.")
                raw_class, confidence = self._cv_fallback(image)
                prediction_source = "fallback"
        else:
            print("[NutrientPrediction] Model unavailable. Fallback mode active (OpenCV color heuristics).")
            raw_class, confidence = self._cv_fallback(image)
            prediction_source = "fallback"

        display_condition = CONDITION_DISPLAY_NAMES.get(raw_class, raw_class)
        recommendation = RECOMMENDATIONS.get(raw_class, "Maintain current nutrient schedule.")
        t_elapsed = time.perf_counter() - t0

        print(f"[Nutrient Debug] condition={display_condition}, confidence={confidence:.4f}, source={prediction_source}")

        if confidence < 0.50:
            result = {
                "condition": "Uncertain",
                "confidence": round(confidence, 2),
                "recommendation": "Low confidence. Please upload a clearer leaf image.",
                "prediction_source": prediction_source
            }
        else:
            result = {
                "condition": display_condition,
                "confidence": round(confidence, 2),
                "recommendation": recommendation,
                "prediction_source": prediction_source
            }

        return result, t_elapsed

    def _cv_fallback(self, image):
        img_arr = np.array(image.resize((100, 100)), dtype=float)
        r = np.mean(img_arr[:, :, 0])
        g = np.mean(img_arr[:, :, 1])
        b = np.mean(img_arr[:, :, 2])
        
        if g > r * 1.15 and g > b * 1.15:
            raw_class = 'healthy'
            confidence = 0.92
        elif r > g * 0.95:
            raw_class = 'nitrogen_deficiency'
            confidence = 0.90
        elif b > g * 0.7:
            raw_class = 'phosphorus_deficiency'
            confidence = 0.88
        else:
            raw_class = 'potassium_deficiency'
            confidence = 0.89
        return raw_class, confidence

nutrient_service = NutrientPredictionService()
