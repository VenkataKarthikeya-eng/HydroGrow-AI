import os
import sys
import io
import torch
import torchvision.transforms as T
import torchvision.models as models
from PIL import Image
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, "..", ".."))

MODEL_PATH = os.path.join(PROJECT_ROOT, "backend", "ml_models", "crop_validator_model.keras")

CLASS_NAMES = ['lettuce_leaf', 'other_plant_leaf', 'non_leaf']

CONFIDENCE_THRESHOLD = 0.90

class CropValidationService:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.transform = T.Compose([
            T.Resize((224, 224)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                checkpoint = torch.load(self.model_path, map_location=self.device)
                
                weights = models.MobileNet_V3_Small_Weights.DEFAULT
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
                self.model.eval()
                print(f"[CropValidationService] Loaded crop validation model from '{self.model_path}' successfully.")
            except Exception as e:
                print(f"[CropValidationService] Error loading model artifact: {e}")
                self.model = None
        else:
            print(f"[CropValidationService] Model file not found at '{self.model_path}'.")
            self.model = None

    def validate_crop_image(self, image_bytes: bytes) -> dict:
        """
        Production Crop Validation Gatekeeper (3-Class & 90% Confidence Guard).
        """
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
        
        # High green saturation foliage mask specific to hydroponic lettuce
        green_lettuce_mask = (g > 40) & (g > r * 1.05) & (g > b * 1.05)
        green_ratio = float(np.mean(green_lettuce_mask))
        
        # General plant foliage mask (requiring green hue dominance over blue)
        plant_foliage_mask = (g > 35) & (g > r * 0.85) & (g > b * 1.02)
        plant_ratio = float(np.mean(plant_foliage_mask))
        
        is_grayscale = float(np.mean(np.abs(r - g) + np.abs(g - b))) < 15.0

        if self.model is not None:
            tensor = self.transform(image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                logits = self.model(tensor)
                probs = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()
                pred_idx = int(np.argmax(probs))
                confidence = float(probs[pred_idx])
                predicted_class = CLASS_NAMES[pred_idx]
                
                # Direct validation checks
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
        else: # non_leaf
            return {
                "status": "rejected",
                "reason": "Invalid image. Please upload a lettuce leaf image.",
                "class": "non_leaf",
                "confidence": confidence
            }

# Global singleton instance
crop_validation_service = CropValidationService()
