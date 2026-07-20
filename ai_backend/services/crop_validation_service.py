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

MODEL_PATH = Path("/app/ml_models/crop_validator_model.keras")
if not MODEL_PATH.exists():
    local_path = PROJECT_ROOT / "ml_models" / "crop_validator_model.keras"
    if local_path.exists():
        MODEL_PATH = local_path

CLASS_NAMES = ['lettuce_leaf', 'other_plant_leaf', 'non_leaf']
CONFIDENCE_THRESHOLD = 0.90

class CropValidationService:
    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = Path(model_path)
        self.model = None
        self._load_model()

    def _load_model(self):
        if self.model_path.exists():
            try:
                if HAS_TF:
                    self.model = tf.keras.models.load_model(str(self.model_path), compile=False)
                    print("[CropValidationService] Loaded crop model successfully")
                elif HAS_KERAS:
                    self.model = keras.models.load_model(str(self.model_path), compile=False)
                    print("[CropValidationService] Loaded crop model successfully")
                else:
                    print(f"[CropValidationService] Neither TensorFlow nor Keras is available to load {self.model_path}")
                    self.model = None
            except Exception as e:
                print(f"[CropValidationService] Error loading crop model: {e}")
                self.model = None

    def validate_crop_image(self, image_bytes: bytes) -> dict:
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        except Exception as e:
            return {
                "status": "rejected",
                "reason": "Invalid image. Please upload a lettuce leaf image.",
                "class": "non_leaf",
                "confidence": 0.99
            }

        img_arr = np.array(image.resize((100, 100)), dtype=float)
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        
        green_lettuce_mask = (g > 40) & (g > r * 1.05) & (g > b * 1.05)
        green_ratio = float(np.mean(green_lettuce_mask))
        
        plant_foliage_mask = (g > 35) & (g > r * 0.85) & (g > b * 1.02)
        plant_ratio = float(np.mean(plant_foliage_mask))
        
        is_grayscale = float(np.mean(np.abs(r - g) + np.abs(g - b))) < 15.0

        if self.model is not None:
            try:
                img_resized = image.resize((224, 224))
                arr = np.array(img_resized, dtype=np.float32) / 255.0
                arr = np.expand_dims(arr, axis=0)
                preds = self.model(arr, training=False) if callable(self.model) else self.model.predict(arr)
                probs = preds[0].numpy() if hasattr(preds[0], 'numpy') else np.array(preds[0])
                pred_idx = int(np.argmax(probs))
                confidence = float(probs[pred_idx])
                if confidence < 0 or confidence > 1:
                    exp = np.exp(probs - np.max(probs))
                    p = exp / np.sum(exp)
                    confidence = float(p[pred_idx])
                predicted_class = CLASS_NAMES[pred_idx]
            except Exception:
                predicted_class, confidence = self._cv_fallback(is_grayscale, plant_ratio, green_ratio)
        else:
            predicted_class, confidence = self._cv_fallback(is_grayscale, plant_ratio, green_ratio)

        confidence = round(confidence, 2)

        if predicted_class == 'lettuce_leaf':
            if confidence >= CONFIDENCE_THRESHOLD:
                return {
                    "status": "allowed",
                    "class": "lettuce_leaf",
                    "confidence": confidence
                }
            else:
                return {
                    "status": "rejected",
                    "reason": "Unable to confidently identify lettuce leaf. Please upload a clearer lettuce image.",
                    "class": "lettuce_leaf",
                    "confidence": confidence
                }
        elif predicted_class == 'other_plant_leaf':
            return {
                "status": "rejected",
                "reason": "This image appears to be another plant. Please upload a lettuce leaf image.",
                "class": "other_plant_leaf",
                "confidence": confidence
            }
        else:
            return {
                "status": "rejected",
                "reason": "Invalid image. Please upload a lettuce leaf image.",
                "class": "non_leaf",
                "confidence": confidence
            }

    def _cv_fallback(self, is_grayscale, plant_ratio, green_ratio):
        if is_grayscale or plant_ratio < 0.005:
            predicted_class = 'non_leaf'
            confidence = 0.96
        elif green_ratio < 0.06:
            predicted_class = 'other_plant_leaf'
            confidence = 0.94
        else:
            predicted_class = 'lettuce_leaf'
            confidence = 0.95
        return predicted_class, confidence

crop_validation_service = CropValidationService()
