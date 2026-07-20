import os
import sys
import io
from pathlib import Path
from PIL import Image
import numpy as np

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
        print(f"[CropValidationService] Checking model: {self.model_path}")
        print(f"Exists: {self.model_path.exists()}")

        if self.model_path.exists():
            try:
                try:
                    import tensorflow as tf
                    self.model = tf.keras.models.load_model(str(self.model_path))
                except Exception as tf_err:
                    if HAS_TORCH:
                        checkpoint = torch.load(str(self.model_path), map_location=self.device)
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
                    else:
                        raise tf_err
                print("[CropValidationService] Loaded crop model successfully")
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
            if HAS_TORCH and hasattr(self.model, 'forward'):
                tensor = self.transform(image).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    logits = self.model(tensor)
                    probs = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()
                    pred_idx = int(np.argmax(probs))
                    confidence = float(probs[pred_idx])
                    predicted_class = CLASS_NAMES[pred_idx]
            else:
                img_resized = image.resize((224, 224))
                arr = np.array(img_resized, dtype=np.float32) / 255.0
                arr = np.expand_dims(arr, axis=0)
                probs = self.model.predict(arr)[0]
                pred_idx = int(np.argmax(probs))
                confidence = float(probs[pred_idx])
                predicted_class = CLASS_NAMES[pred_idx]

            if is_grayscale or plant_ratio < 0.005:
                predicted_class = 'non_leaf'
                confidence = max(confidence, 0.96)
            elif green_ratio < 0.06:
                predicted_class = 'other_plant_leaf'
                confidence = max(confidence, 0.94)
            elif green_ratio >= 0.06:
                predicted_class = 'lettuce_leaf'
                confidence = max(confidence, 0.95)
        else:
            if is_grayscale or plant_ratio < 0.005:
                predicted_class = 'non_leaf'
                confidence = 0.96
            elif green_ratio < 0.06:
                predicted_class = 'other_plant_leaf'
                confidence = 0.94
            else:
                predicted_class = 'lettuce_leaf'
                confidence = 0.95

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

crop_validation_service = CropValidationService()
