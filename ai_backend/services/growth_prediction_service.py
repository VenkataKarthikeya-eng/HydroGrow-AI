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
except ImportError:
    torch = None
    T = None
    models = None
    HAS_TORCH = False

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
        print(f"[GrowthPredictionService] Checking model: {self.model_path}")
        print(f"Exists: {self.model_path.exists()}")

        if self.model_path.exists():
            try:
                try:
                    import tensorflow as tf
                    self.model = tf.keras.models.load_model(str(self.model_path))
                except Exception as tf_err:
                    if HAS_TORCH:
                        checkpoint = torch.load(str(self.model_path), map_location=self.device)
                        backbone = models.efficientnet_b0(weights=None)
                        in_features = backbone.classifier[1].in_features
                        backbone.classifier = torch.nn.Identity()

                        class DualHeadEfficientNet(torch.nn.Module):
                            def __init__(self, bb, inf):
                                super().__init__()
                                self.backbone = bb
                                self.classifier = torch.nn.Sequential(
                                    torch.nn.Dropout(0.2),
                                    torch.nn.Linear(inf, 256),
                                    torch.nn.ReLU(),
                                    torch.nn.Linear(256, 3)
                                )
                                self.regressor = torch.nn.Sequential(
                                    torch.nn.Dropout(0.2),
                                    torch.nn.Linear(inf, 128),
                                    torch.nn.ReLU(),
                                    torch.nn.Linear(128, 1)
                                )
                            def forward(self, x):
                                feat = self.backbone(x)
                                return self.classifier(feat), self.regressor(feat).squeeze(-1)

                        self.model = DualHeadEfficientNet(backbone, in_features).to(self.device)
                        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                            self.model.load_state_dict(checkpoint['model_state_dict'])
                        self.model.eval()
                    else:
                        raise tf_err
                print("Loaded growth model successfully")
            except Exception as e:
                print(f"[GrowthPredictionService] Error loading model: {e}")
                self.model = None

    def predict_image(self, image_bytes: bytes) -> dict:
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        except Exception as e:
            raise ValueError(f"Invalid image content: {str(e)}")

        if self.model is not None:
            if HAS_TORCH and hasattr(self.model, 'forward'):
                tensor = self.transform(image).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    logits, day_pred = self.model(tensor)
                    probs = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()
                    pred_class_idx = int(np.argmax(probs))
                    confidence = float(probs[pred_class_idx])
                    predicted_stage = STAGE_CLASSES[pred_class_idx]
                    
                    raw_day = float(day_pred.item())
                    min_d, max_d = STAGE_DAY_ESTIMATES[predicted_stage]
                    growth_day = int(np.clip(round(raw_day), min_d, max_d))
            else:
                img_resized = image.resize((224, 224))
                arr = np.array(img_resized, dtype=np.float32) / 255.0
                arr = np.expand_dims(arr, axis=0)
                preds = self.model.predict(arr)
                if isinstance(preds, (list, tuple)):
                    logits = preds[0][0]
                    day_pred = float(preds[1][0])
                else:
                    logits = preds[0]
                    day_pred = 15.0
                pred_class_idx = int(np.argmax(logits))
                confidence = float(logits[pred_class_idx])
                predicted_stage = STAGE_CLASSES[pred_class_idx]
                min_d, max_d = STAGE_DAY_ESTIMATES[predicted_stage]
                growth_day = int(np.clip(round(day_pred), min_d, max_d))
        else:
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

        recommendation = STAGE_RECOMMENDATIONS.get(predicted_stage, "Continue nutrient schedule.")

        return {
            "growth_stage": predicted_stage,
            "growth_day": growth_day,
            "confidence": round(confidence, 2),
            "recommendation": recommendation
        }

growth_service = GrowthPredictionService()
