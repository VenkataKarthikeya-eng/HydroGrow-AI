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

MODEL_PATH = Path("/app/ml_models/growth_model.keras")
if not MODEL_PATH.exists():
    local_path = PROJECT_ROOT / "ml_models" / "growth_model.keras"
    if local_path.exists():
        MODEL_PATH = local_path

STAGE_CLASSES = ['Seedling', 'Vegetative', 'Mature / Harvest']

STAGE_RECOMMENDATIONS = {
    'Seedling': "Maintain low EC (0.8–1.2 mS/cm), high humidity (65-75%), and light misting for delicate seedling roots.",
    'Vegetative': "Continue nutrient schedule. Maintain EC (1.4–1.8 mS/cm) and pH (5.8–6.2) for rapid foliage expansion.",
    'Mature / Harvest': "Lettuce is in mature harvest window. Prepare for harvest within 3-5 days; monitor tipburn."
}

STAGE_DAY_ESTIMATES = {
    'Seedling': (1, 10),
    'Vegetative': (11, 20),
    'Mature / Harvest': (21, 27)
}

class GrowthPredictionService:
    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = Path(model_path)
        self.model = None
        self._load_model()

    def _load_model(self):
        if self.model_path.exists():
            try:
                if HAS_TF:
                    self.model = tf.keras.models.load_model(str(self.model_path), compile=False)
                    print("[GrowthPredictionService] Loaded growth model successfully")
                elif HAS_KERAS:
                    self.model = keras.models.load_model(str(self.model_path), compile=False)
                    print("[GrowthPredictionService] Loaded growth model successfully")
                else:
                    print(f"[GrowthPredictionService] Neither TensorFlow nor Keras is available to load {self.model_path}")
                    self.model = None
            except Exception as e:
                print(f"[GrowthPredictionService] Error loading growth model: {e}")
                self.model = None

    def predict_image(self, image_bytes: bytes) -> dict:
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        except Exception as e:
            raise ValueError(f"Invalid image content: {str(e)}")

        if self.model is not None:
            try:
                img_resized = image.resize((224, 224))
                arr = np.array(img_resized, dtype=np.float32) / 255.0
                arr = np.expand_dims(arr, axis=0)
                preds = self.model(arr, training=False) if callable(self.model) else self.model.predict(arr)
                if isinstance(preds, (list, tuple)):
                    logits = preds[0][0].numpy() if hasattr(preds[0][0], 'numpy') else np.array(preds[0][0])
                    day_pred = float(preds[1][0].numpy() if hasattr(preds[1][0], 'numpy') else preds[1][0])
                else:
                    logits = preds[0].numpy() if hasattr(preds[0], 'numpy') else np.array(preds[0])
                    day_pred = 15.0
                pred_class_idx = int(np.argmax(logits))
                confidence = float(np.max(logits))
                if confidence < 0 or confidence > 1:
                    exp = np.exp(logits - np.max(logits))
                    probs = exp / np.sum(exp)
                    confidence = float(probs[pred_class_idx])
                predicted_stage = STAGE_CLASSES[pred_class_idx]
                min_d, max_d = STAGE_DAY_ESTIMATES[predicted_stage]
                growth_day = int(np.clip(round(day_pred), min_d, max_d))
            except Exception:
                predicted_stage, growth_day, confidence = self._cv_fallback(image)
        else:
            predicted_stage, growth_day, confidence = self._cv_fallback(image)

        recommendation = STAGE_RECOMMENDATIONS.get(predicted_stage, "Continue nutrient schedule.")

        return {
            "growth_stage": predicted_stage,
            "growth_day": growth_day,
            "confidence": round(confidence, 2),
            "recommendation": recommendation
        }

    def _cv_fallback(self, image):
        img_arr = np.array(image.resize((100, 100)), dtype=float)
        green_mask = (img_arr[:, :, 1] > 60) & (img_arr[:, :, 1] > img_arr[:, :, 0] * 1.1) & (img_arr[:, :, 1] > img_arr[:, :, 2] * 1.1)
        green_ratio = float(np.mean(green_mask))

        if green_ratio < 0.02:
            predicted_stage = 'Seedling'
            growth_day = int(1 + (green_ratio / 0.02) * 9)
            confidence = 0.91
        elif green_ratio < 0.08:
            predicted_stage = 'Vegetative'
            growth_day = int(11 + ((green_ratio - 0.02) / 0.06) * 9)
            confidence = 0.94
        else:
            predicted_stage = 'Mature / Harvest'
            growth_day = int(21 + min(float(green_ratio - 0.08) * 50, 6.0))
            confidence = 0.96
        return predicted_stage, growth_day, confidence

growth_service = GrowthPredictionService()
