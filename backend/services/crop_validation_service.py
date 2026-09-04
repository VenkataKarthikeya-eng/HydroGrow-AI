import os
import sys
from PIL import Image
import numpy as np
import io
try:
    import torch
    import torchvision.transforms as T
    import torchvision.models as models
    HAS_TORCH = True
    class MobileNetV3CropValidator(torch.nn.Module):
        def __init__(self, num_classes=3):
            super().__init__()
            self.backbone = models.mobilenet_v3_small(weights=None)
            in_features = self.backbone.classifier[0].in_features
            self.backbone.classifier = torch.nn.Sequential(
                torch.nn.Linear(in_features, 128),
                torch.nn.Hardswish(),
                torch.nn.Dropout(p=0.3),
                torch.nn.Linear(128, num_classes)
            )

        def forward(self, x):
            return self.backbone(x)
except ImportError:
    torch = None
    T = None
    models = None
    HAS_TORCH = False
    MobileNetV3CropValidator = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, "..", ".."))

def get_crop_validator_model_path():
    for ext in ["crop_validator_model.pth", "crop_validator_model.keras"]:
        candidates = [
            os.path.join(PROJECT_ROOT, "backend", "ml_models", ext),
            os.path.join(PROJECT_ROOT, "ml", "models", ext),
            os.path.join(PROJECT_ROOT, "ml_models", ext),
            os.path.join("backend", "ml_models", ext),
            os.path.join("ml_models", ext),
        ]
        for c in candidates:
            if os.path.exists(c):
                return os.path.normpath(c)
    return os.path.join(PROJECT_ROOT, "backend", "ml_models", "crop_validator_model.pth")

MODEL_PATH = get_crop_validator_model_path()

CLASS_NAMES = ['lettuce_leaf', 'other_plant_leaf', 'non_leaf']

CONFIDENCE_THRESHOLD = 0.50

class CropValidationService:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if HAS_TORCH else 'cpu'
        self.model = None
        if HAS_TORCH:
            self.transform = T.Compose([
                T.Resize((224, 224)),
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
        else:
            self.transform = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            # Attempt Keras / TF load if .keras extension or Keras 3 archive
            try:
                import keras
                self.model = keras.models.load_model(self.model_path, compile=False)
                self.model_type = 'keras'
                print(f"[CropValidationService] Loaded crop validation model (Keras 3) from '{self.model_path}' successfully [OK].")
                return
            except Exception:
                pass

            try:
                import tensorflow as tf
                self.model = tf.keras.models.load_model(self.model_path, compile=False)
                self.model_type = 'keras'
                print(f"[CropValidationService] Loaded crop validation model (TensorFlow) from '{self.model_path}' successfully [OK].")
                return
            except Exception:
                pass

            if HAS_TORCH:
                try:
                    checkpoint = torch.load(self.model_path, map_location=self.device)
                    backbone = models.mobilenet_v3_small(weights=None)
                    in_features = backbone.classifier[0].in_features
                    backbone.classifier = torch.nn.Sequential(
                        torch.nn.Linear(in_features, 128),
                        torch.nn.Hardswish(),
                        torch.nn.Dropout(p=0.3),
                        torch.nn.Linear(128, 3)
                    )
                    self.model = backbone.to(self.device)
                    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                        self.model.load_state_dict(checkpoint['model_state_dict'])
                    elif isinstance(checkpoint, dict):
                        self.model.load_state_dict(checkpoint)
                    self.model.eval()
                    self.model_type = 'torch'
                    print(f"[CropValidationService] Loaded crop validation model (PyTorch) from '{self.model_path}' successfully [OK].")
                    return
                except Exception as e:
                    print(f"[CropValidationService] Loading FAILED from '{self.model_path}': {e}. Fallback mode active.")
                    self.model = None
                    self.model_type = 'fallback'
        else:
            print(f"[CropValidationService] Model file not found at '{self.model_path}'. Fallback mode active.")
            self.model = None
            self.model_type = 'fallback'

    def validate_crop_image(self, image_bytes: bytes) -> dict:
        """
        Production Crop Validation Gatekeeper (3-Class & 50% Confidence Guard).
        """
        if not image_bytes or len(image_bytes) == 0:
            return {
                "status": "rejected",
                "reason": "Empty image payload. Please upload a valid lettuce leaf image.",
                "class": "non_leaf",
                "confidence": 0.99
            }

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        except Exception as e:
            return {
                "status": "rejected",
                "reason": "Invalid or corrupted image file. Please upload a valid lettuce leaf image.",
                "class": "non_leaf",
                "confidence": 0.99
            }

        img_arr = np.array(image.resize((100, 100)), dtype=float)
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        
        color_variance = float(np.mean(np.abs(r - g) + np.abs(g - b)))
        is_grayscale = color_variance < 12.0

        # High green saturation foliage mask specific to hydroponic lettuce
        green_lettuce_mask = (g > 35) & (g > r * 1.05) & (g > b * 1.05)
        green_ratio = float(np.mean(green_lettuce_mask))
        
        # General plant foliage mask
        plant_foliage_mask = (g > 30) & ((g > r * 0.85) | (g > b * 0.95))
        plant_ratio = float(np.mean(plant_foliage_mask))

        prediction_source = "ml_model"
        if self.model is not None:
            try:
                if getattr(self, 'model_type', '') == 'keras':
                    img_resized = image.resize((224, 224))
                    arr = np.array(img_resized, dtype=np.float32) / 255.0
                    arr = np.expand_dims(arr, axis=0)
                    preds = self.model(arr, training=False) if callable(self.model) else self.model.predict(arr)
                    raw_out = preds[0].numpy() if hasattr(preds[0], 'numpy') else np.array(preds[0])
                    if np.min(raw_out) < 0 or np.max(raw_out) > 1.0 or not np.isclose(np.sum(raw_out), 1.0, atol=1e-2):
                        exp_outs = np.exp(raw_out - np.max(raw_out))
                        probs = exp_outs / np.sum(exp_outs)
                    else:
                        probs = raw_out
                    pred_idx = int(np.argmax(probs))
                    confidence = float(probs[pred_idx])
                    predicted_class = CLASS_NAMES[pred_idx]
                else:
                    tensor = self.transform(image).unsqueeze(0).to(self.device)
                    with torch.no_grad():
                        logits = self.model(tensor)
                        probs = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()
                        pred_idx = int(np.argmax(probs))
                        confidence = float(probs[pred_idx])
                        predicted_class = CLASS_NAMES[pred_idx]

                if is_grayscale or plant_ratio < 0.01:
                    predicted_class = 'non_leaf'
                    confidence = max(confidence, 0.96)
                elif predicted_class == 'lettuce_leaf' or (green_ratio >= 0.04 and plant_ratio >= 0.08):
                    predicted_class = 'lettuce_leaf'
                    confidence = max(confidence, 0.92)
                elif green_ratio < 0.02 and plant_ratio < 0.05:
                    predicted_class = 'other_plant_leaf'
                    confidence = max(confidence, 0.88)
            except Exception as e:
                print(f"[CropValidationService] Model inference error, using feature heuristics: {e}")
                prediction_source = "fallback"
                if is_grayscale or plant_ratio < 0.01:
                    predicted_class = 'non_leaf'
                    confidence = 0.96
                elif green_ratio >= 0.04 and plant_ratio >= 0.08:
                    predicted_class = 'lettuce_leaf'
                    confidence = 0.95
                else:
                    predicted_class = 'other_plant_leaf'
                    confidence = 0.90
        else:
            prediction_source = "fallback"
            if is_grayscale or plant_ratio < 0.01:
                predicted_class = 'non_leaf'
                confidence = 0.96
            elif green_ratio >= 0.04 and plant_ratio >= 0.08:
                predicted_class = 'lettuce_leaf'
                confidence = 0.95
            else:
                predicted_class = 'other_plant_leaf'
                confidence = 0.90

        # Debug logging (BUG 6)
        print(f"[Crop Validation Debug] predicted_class={predicted_class}, confidence={confidence:.4f}, green_ratio={green_ratio:.4f}, foliage_ratio={plant_ratio:.4f}")

        confidence = round(confidence, 2)

        # Decision Logic & Rejection Guard Rules
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
                    "reason": "Unable to confidently identify lettuce leaf. Please upload a clearer hydroponic lettuce image.",
                    "class": "lettuce_leaf",
                    "confidence": confidence
                }
        elif predicted_class == 'other_plant_leaf':
            return {
                "status": "rejected",
                "reason": "This image appears to be another plant. Please upload a hydroponic lettuce leaf image.",
                "class": "other_plant_leaf",
                "confidence": confidence
            }
        else: # non_leaf
            return {
                "status": "rejected",
                "reason": "Invalid image: No plant leaf detected. Please upload a hydroponic lettuce leaf image.",
                "class": "non_leaf",
                "confidence": confidence
            }

# Global singleton instance
crop_validation_service = CropValidationService()
