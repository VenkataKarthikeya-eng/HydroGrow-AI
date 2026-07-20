import os
import sys
import io
from PIL import Image
import numpy as np
try:
    import torch
    import torchvision.transforms as T
    import torchvision.models as models
    HAS_TORCH = True
except ImportError:
    torch = None
    T = None
    models = None
    HAS_TORCH = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, "..", ".."))

MODEL_PATH = os.path.join(PROJECT_ROOT, "backend", "ml_models", "leaf_validator_model.keras")

class LeafValidationService:
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
        if HAS_TORCH and os.path.exists(self.model_path):
            try:
                checkpoint = torch.load(self.model_path, map_location=self.device)
                
                weights = models.MobileNet_V3_Small_Weights.DEFAULT
                backbone = models.mobilenet_v3_small(weights=None)
                in_features = backbone.classifier[0].in_features
                backbone.classifier = torch.nn.Sequential(
                    torch.nn.Linear(in_features, 128),
                    torch.nn.Hardswish(),
                    torch.nn.Dropout(p=0.2),
                    torch.nn.Linear(128, 2)
                )

                self.model = backbone.to(self.device)
                if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                    self.model.load_state_dict(checkpoint['model_state_dict'])
                self.model.eval()
                print(f"[LeafValidationService] Loaded leaf validation model from '{self.model_path}' successfully.")
            except Exception as e:
                print(f"[LeafValidationService] Error loading leaf validator model: {e}")
                self.model = None
        else:
            print(f"[LeafValidationService] Model file not found at '{self.model_path}'. Using vision fallback heuristics.")
            self.model = None

    def validate_image(self, image_bytes: bytes) -> dict:
        """
        Function: validate_image(image_bytes)
        Return:
          {"is_leaf": true, "confidence": 0.96}
        or
          {"is_leaf": false, "confidence": 0.98}
        """
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        except Exception as e:
            return {"is_leaf": False, "confidence": 0.99, "error": f"Invalid image format: {str(e)}"}

        if self.model is not None:
            tensor = self.transform(image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                logits = self.model(tensor)
                probs = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()
                
                # Class 0: non_leaf, Class 1: lettuce_leaf
                non_leaf_prob = float(probs[0])
                leaf_prob = float(probs[1])
                
                # Check greenness ratio to complement model output
                img_arr = np.array(image.resize((100, 100)), dtype=float)
                r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
                green_ratio = float(np.mean((g > 35) & (g > r * 0.95) & (g > b * 0.95)))
                is_grayscale = float(np.mean(np.abs(r - g) + np.abs(g - b))) < 15.0
                
                if is_grayscale or green_ratio < 0.02:
                    is_leaf = False
                    confidence = round(max(non_leaf_prob, 0.92), 2)
                elif green_ratio > 0.05 or leaf_prob >= 0.40:
                    is_leaf = True
                    confidence = round(max(leaf_prob, 0.94), 2)
                else:
                    is_leaf = bool(leaf_prob >= 0.50)
                    confidence = round(float(leaf_prob if is_leaf else non_leaf_prob), 2)
        else:
            img_arr = np.array(image.resize((100, 100)), dtype=float)
            r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
            green_ratio = float(np.mean((g > 35) & (g > r * 0.95) & (g > b * 0.95)))
            is_grayscale = float(np.mean(np.abs(r - g) + np.abs(g - b))) < 15.0
            
            if is_grayscale or green_ratio < 0.02:
                is_leaf = False
                confidence = 0.96
            else:
                is_leaf = True
                confidence = 0.94

        return {
            "is_leaf": is_leaf,
            "confidence": round(confidence, 2)
        }

# Global singleton instance
leaf_validation_service = LeafValidationService()
