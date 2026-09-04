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
    class MobileNetV3NutrientModel(torch.nn.Module):
        def __init__(self, num_classes=4):
            super().__init__()
            self.backbone = models.mobilenet_v3_small(weights=None)
            in_features = self.backbone.classifier[0].in_features
            self.backbone.classifier = torch.nn.Sequential(
                torch.nn.Linear(in_features, 256),
                torch.nn.Hardswish(),
                torch.nn.Dropout(p=0.3),
                torch.nn.Linear(256, num_classes)
            )

        def forward(self, x):
            return self.backbone(x)
except ImportError:
    torch = None
    T = None
    models = None
    HAS_TORCH = False
    MobileNetV3NutrientModel = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, "..", ".."))

def get_nutrient_model_path():
    for ext in ["nutrient_model.pth", "nutrient_model.keras"]:
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
    return os.path.join(PROJECT_ROOT, "backend", "ml_models", "nutrient_model.pth")

MODEL_PATH = get_nutrient_model_path()

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
            try:
                import keras
                self.model = keras.models.load_model(self.model_path, compile=False)
                self.model_type = 'keras'
                print(f"[NutrientPredictionService] Loaded nutrient model (Keras 3) from '{self.model_path}' successfully [OK].")
                return
            except Exception:
                pass

            try:
                import tensorflow as tf
                self.model = tf.keras.models.load_model(self.model_path, compile=False)
                self.model_type = 'keras'
                print(f"[NutrientPredictionService] Loaded nutrient model (TensorFlow) from '{self.model_path}' successfully [OK].")
                return
            except Exception:
                pass

            if HAS_TORCH:
                try:
                    checkpoint = torch.load(self.model_path, map_location=self.device)
                    self.model = MobileNetV3NutrientModel(num_classes=4).to(self.device)
                    
                    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                        self.model.load_state_dict(checkpoint['model_state_dict'])
                    elif isinstance(checkpoint, dict):
                        self.model.load_state_dict(checkpoint)
                        
                    self.model.eval()
                    self.model_type = 'torch'
                    print(f"[NutrientPredictionService] Loaded nutrient model (PyTorch) from '{self.model_path}' successfully [OK].")
                    return
                except Exception as e:
                    print(f"[NutrientPredictionService] Loading FAILED from '{self.model_path}': {e}. Fallback mode active.")
                    self.model = None
                    self.model_type = 'fallback'
        else:
            print(f"[NutrientPredictionService] Model file not found at '{self.model_path}'. Fallback mode active.")
            self.model = None
            self.model_type = 'fallback'

    def predict_image(self, image_bytes: bytes) -> dict:
        """
        Input: Plant leaf image bytes
        Output: JSON matching specification:
        {
          "condition": "Nitrogen Deficiency",
          "confidence": 0.91,
          "recommendation": "Increase nitrogen availability and monitor leaf color."
        }
        """
        if not image_bytes or len(image_bytes) == 0:
            raise ValueError("Empty image payload provided.")

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        except Exception as e:
            raise ValueError(f"Invalid image content: {str(e)}")

        prediction_source = "ml_model"
        if self.model is not None:
            try:
                if getattr(self, 'model_type', '') == 'keras':
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
                    raw_class = CLASS_NAMES[pred_idx]
                else:
                    tensor = self.transform(image).unsqueeze(0).to(self.device)
                    with torch.no_grad():
                        logits = self.model(tensor)
                        probs = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()
                        pred_idx = int(np.argmax(probs))
                        confidence = float(probs[pred_idx])
                        raw_class = CLASS_NAMES[pred_idx]
            except Exception as e:
                print(f"[NutrientPredictionService] Inference error, falling back to color heuristics: {e}")
                raw_class, confidence = self._heuristic_fallback(image)
                prediction_source = "fallback"
        else:
            raw_class, confidence = self._heuristic_fallback(image)
            prediction_source = "fallback"

        display_condition = CONDITION_DISPLAY_NAMES.get(raw_class, raw_class)
        recommendation = RECOMMENDATIONS.get(raw_class, "Maintain current nutrient schedule.")

        print(f"[Nutrient Debug] condition={display_condition}, confidence={confidence:.4f}, source={prediction_source}")

        if confidence < 0.50:
            return {
                "condition": "Uncertain",
                "confidence": round(confidence, 2),
                "recommendation": "Low confidence. Please upload a clearer leaf image.",
                "prediction_source": prediction_source
            }

        return {
            "condition": display_condition,
            "confidence": round(confidence, 2),
            "recommendation": recommendation,
            "prediction_source": prediction_source
        }

    def _heuristic_fallback(self, image: Image.Image):
        img_arr = np.array(image.resize((100, 100)), dtype=float)
        r = np.mean(img_arr[:, :, 0])
        g = np.mean(img_arr[:, :, 1])
        b = np.mean(img_arr[:, :, 2])
        
        if g > r * 1.15 and g > b * 1.15:
            raw_class = 'healthy'
            confidence = 0.92
        elif r > g * 0.95: # Yellowing chlorosis
            raw_class = 'nitrogen_deficiency'
            confidence = 0.90
        elif b > g * 0.7: # Dark purple/brownish edges
            raw_class = 'phosphorus_deficiency'
            confidence = 0.88
        else:
            raw_class = 'potassium_deficiency'
            confidence = 0.89

        return raw_class, confidence

# Global singleton instance
nutrient_service = NutrientPredictionService()
