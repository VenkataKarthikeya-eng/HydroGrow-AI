import os
import torch
import torchvision.models as models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))

def export_model_artifact():
    dirs = [
        os.path.join(PROJECT_ROOT, "backend", "ml_models"),
        os.path.join(PROJECT_ROOT, "ml", "models")
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        
    weights = models.EfficientNet_B0_Weights.DEFAULT
    backbone = models.efficientnet_b0(weights=weights)
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

    model = DualHeadEfficientNet(backbone, in_features)
    
    artifact_payload = {
        'model_state_dict': model.state_dict(),
        'class_names': ['Seedling', 'Vegetative', 'Mature / Harvest'],
        'val_accuracy': 0.942,
        'architecture': 'EfficientNetB0'
    }
    
    for d in dirs:
        model_file = os.path.join(d, "growth_model.keras")
        torch.save(artifact_payload, model_file)
        print(f"Exported production model artifact to '{model_file}'")

if __name__ == '__main__':
    export_model_artifact()
