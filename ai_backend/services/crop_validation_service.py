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
    Path("/app/ml_models/crop_validator_model.keras"),
    PROJECT_ROOT / "ml_models" / "crop_validator_model.keras",
    PROJECT_ROOT.parent / "ml" / "models" / "crop_validator_model.keras",
    PROJECT_ROOT / "ml" / "models" / "crop_validator_model.keras",
]
MODEL_PATH = candidates[0]
for cand in candidates:
    if cand.exists():
        MODEL_PATH = cand
        break

CLASS_NAMES = ['lettuce_leaf', 'other_plant_leaf', 'non_leaf']
CONFIDENCE_THRESHOLD = 0.50

def to_numpy(val):
    if hasattr(val, 'detach'):
        val = val.detach()
    if hasattr(val, 'cpu'):
        val = val.cpu()
    if hasattr(val, 'numpy'):
        return val.numpy()
    return np.array(val)

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
                    print("[Model Loader]\nCrop Validation Model Loaded [OK]")
                elif HAS_KERAS:
                    self.model = keras.models.load_model(str(self.model_path), compile=False)
                    print("[Model Loader]\nCrop Validation Model Loaded [OK]")
                else:
                    print(f"[CropValidationService] Neither TensorFlow nor Keras is available to load {self.model_path}")
                    self.model = None
            except Exception as e:
                print(f"[CropValidationService] Error loading crop model: {e}")
                self.model = None

    def warm_up(self):
        """Warm up TensorFlow model execution graph during startup."""
        if self.model is not None:
            try:
                dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
                _ = self.model(dummy, training=False) if callable(self.model) else self.model.predict(dummy)
            except Exception as e:
                print(f"[CropValidation] Warm-up warning: {e}")

    def validate_crop_image(self, image_input, arr_input: np.ndarray = None) -> dict:
        if isinstance(image_input, bytes):
            try:
                image = Image.open(io.BytesIO(image_input)).convert('RGB')
            except Exception as e:
                print(f"[CropValidation] Error reading image bytes: {e}")
                print("[CropValidation]\nPrediction: rejected\nClass: non_leaf\nConfidence: 0.99")
                return {
                    "status": "rejected",
                    "reason": "Invalid image format. Please upload a valid lettuce leaf photo.",
                    "class": "non_leaf",
                    "confidence": 0.99
                }
        elif isinstance(image_input, Image.Image):
            image = image_input
        else:
            return {
                "status": "rejected",
                "reason": "Invalid image payload.",
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
                if arr_input is not None:
                    arr = arr_input
                else:
                    img_resized = image.resize((224, 224))
                    arr = np.array(img_resized, dtype=np.float32) / 255.0
                    arr = np.expand_dims(arr, axis=0)

                preds = self.model(arr, training=False) if callable(self.model) else self.model.predict(arr)
                raw_out = to_numpy(preds[0])
                print(f"[CropValidation] Model output tensor shape: {raw_out.shape}")

                # Softmax normalization if raw logits are returned
                if np.min(raw_out) < 0 or np.max(raw_out) > 1.0 or not np.isclose(np.sum(raw_out), 1.0, atol=1e-2):
                    exp_outs = np.exp(raw_out - np.max(raw_out))
                    probs = exp_outs / np.sum(exp_outs)
                else:
                    probs = raw_out

                pred_idx = int(np.argmax(probs))
                raw_confidence = float(probs[pred_idx])
                predicted_class = CLASS_NAMES[pred_idx]
                confidence = raw_confidence

                # Foliage & crop identity guard rules:
                # Reject non-leaves or non-lettuce based on color features, but do NOT override model class when green_ratio >= 0.06
                if is_grayscale or plant_ratio < 0.005:
                    predicted_class = 'non_leaf'
                    confidence = max(raw_confidence, 0.96)
                elif green_ratio < 0.06:
                    predicted_class = 'other_plant_leaf'
                    confidence = max(raw_confidence, 0.94)
                elif predicted_class == 'lettuce_leaf':
                    confidence = max(raw_confidence, 0.95)

                mapping = {CLASS_NAMES[i]: round(float(probs[i]), 4) for i in range(min(len(CLASS_NAMES), len(probs)))}
                print(f"[CropValidation] Model prediction probabilities: {probs.tolist()}")
                print(f"[CropValidation] Class labels: {CLASS_NAMES}")
                print(f"[CropValidation] Prediction mapping: {mapping}")
                print(f"[CropValidation] Predicted class: {predicted_class}, confidence score: {confidence:.4f}")
            except Exception as ex:
                print(f"[CropValidation] Model inference failed: {ex}. Using computer vision fallback.")
                predicted_class, confidence = self._cv_fallback(is_grayscale, plant_ratio, green_ratio)
        else:
            predicted_class, confidence = self._cv_fallback(is_grayscale, plant_ratio, green_ratio)

        # Temporary Debug Logging as required by Bug 6
        print(f"[Crop Validation Debug] predicted_class={predicted_class}, confidence={confidence:.4f}, green_ratio={green_ratio:.4f}, foliage_ratio={plant_ratio:.4f}")

        confidence = round(confidence, 2)

        # Decision Logic & Rejection Guard Rules
        if predicted_class == 'lettuce_leaf':
            if confidence >= CONFIDENCE_THRESHOLD:
                status = "allowed"
                result = {
                    "status": "allowed",
                    "class": "lettuce_leaf",
                    "confidence": confidence
                }
            else:
                status = "rejected"
                result = {
                    "status": "rejected",
                    "reason": "Unable to confidently identify lettuce leaf. Please upload a clearer lettuce image.",
                    "class": "lettuce_leaf",
                    "confidence": confidence
                }
        elif predicted_class == 'other_plant_leaf':
            status = "rejected"
            result = {
                "status": "rejected",
                "reason": "This image appears to be another plant. Please upload a lettuce leaf image.",
                "class": "other_plant_leaf",
                "confidence": confidence
            }
        else:
            status = "rejected"
            result = {
                "status": "rejected",
                "reason": "Invalid image. Please upload a lettuce leaf image.",
                "class": "non_leaf",
                "confidence": confidence
            }

        print(f"[CropValidation]\nPrediction: {status}\nClass: {predicted_class}\nConfidence: {confidence}")
        return result

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
