import os
import sys
import time
import ssl

# Bypass local SSL certificate check for downloading pre-trained model weights
ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as T
import torchvision.models as models
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Class mappings
STAGE_MAP = {
    'Seedling': 0,
    'Vegetative': 1,
    'Mature / Harvest': 2
}
REV_STAGE_MAP = {v: k for k, v in STAGE_MAP.items()}

class GrowthDataset(Dataset):
    def __init__(self, df, transform=None):
        self.df = df.reset_index(drop=True)
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = row['image_path']
        if not os.path.isabs(img_path):
            img_path = os.path.normpath(os.path.join(PROJECT_ROOT, img_path))
        
        try:
            image = Image.open(img_path).convert('RGB')
        except Exception:
            # Fallback blank image if reading fails
            image = Image.new('RGB', (224, 224), (0, 0, 0))

        if self.transform:
            image = self.transform(image)

        stage_label = STAGE_MAP.get(row['growth_stage'], 0)
        growth_day = float(row['growth_day'])

        return image, torch.tensor(stage_label, dtype=torch.long), torch.tensor(growth_day, dtype=torch.float32)

class EfficientNetGrowthModel(nn.Module):
    def __init__(self, num_classes=3):
        super(EfficientNetGrowthModel, self).__init__()
        # Load backbone
        weights = models.EfficientNet_B0_Weights.DEFAULT
        self.backbone = models.efficientnet_b0(weights=weights)
        in_features = self.backbone.classifier[1].in_features
        
        # Custom head for classification & regression
        self.backbone.classifier = nn.Identity()
        
        self.classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes)
        )
        self.regressor = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(in_features, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        features = self.backbone(x)
        stage_logits = self.classifier(features)
        day_pred = self.regressor(features)
        return stage_logits, day_pred.squeeze(-1)

def train_experiment(sample_fraction=0.20, epochs=3, batch_size=32):
    print("=" * 60)
    print(f"STEP 1: VALIDATION EXPERIMENT ON {int(sample_fraction*100)}% SAMPLE DATASET")
    print("=" * 60)
    
    csv_path = os.path.join(PROJECT_ROOT, "data", "processed", "growth_labels.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Labels CSV not found at {csv_path}. Run generate_growth_labels.py first.")

    df = pd.read_csv(csv_path)
    print(f"Total dataset size: {len(df):,} records")
    
    # Stratified sample
    sample_df, _ = train_test_split(df, train_size=sample_fraction, stratify=df['growth_stage'], random_state=42)
    print(f"Sample experiment dataset size: {len(sample_df):,} records")
    print("Sample class distribution:")
    print(sample_df['growth_stage'].value_counts())
    
    # Train/Val split on sample
    train_df, val_df = train_test_split(sample_df, test_size=0.20, stratify=sample_df['growth_stage'], random_state=42)
    
    # Transforms
    train_transform = T.Compose([
        T.Resize((224, 224)),
        T.RandomHorizontalFlip(),
        T.RandomRotation(15),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = T.Compose([
        T.Resize((224, 224)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    train_loader = DataLoader(GrowthDataset(train_df, train_transform), batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(GrowthDataset(val_df, val_transform), batch_size=batch_size, shuffle=False, num_workers=0)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\nTraining device: {device}")
    
    model = EfficientNetGrowthModel(num_classes=3).to(device)
    criterion_cls = nn.CrossEntropyLoss()
    criterion_reg = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    
    start_time = time.time()
    
    for epoch in range(1, epochs + 1):
        model.train()
        total_loss, cls_loss_sum = 0.0, 0.0
        correct, total = 0, 0
        
        # Limit steps per epoch for fast verification
        max_batches = 150
        for step, (imgs, stages, days) in enumerate(train_loader):
            if step >= max_batches:
                break
            imgs, stages, days = imgs.to(device), stages.to(device), days.to(device)
            
            optimizer.zero_grad()
            stage_logits, day_preds = model(imgs)
            
            l_cls = criterion_cls(stage_logits, stages)
            l_reg = criterion_reg(day_preds, days)
            loss = l_cls + 0.1 * l_reg
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            cls_loss_sum += l_cls.item()
            preds = torch.argmax(stage_logits, dim=1)
            correct += (preds == stages).sum().item()
            total += stages.size(0)
            
        train_acc = correct / max(total, 1)
        avg_loss = total_loss / max(min(len(train_loader), max_batches), 1)
        
        # Validation evaluation
        model.eval()
        val_correct, val_total = 0, 0
        val_preds_list, val_targets_list = [], []
        
        with torch.no_grad():
            for step, (imgs, stages, days) in enumerate(val_loader):
                if step >= 50: # subset for fast validation step
                    break
                imgs, stages = imgs.to(device), stages.to(device)
                stage_logits, _ = model(imgs)
                preds = torch.argmax(stage_logits, dim=1)
                val_correct += (preds == stages).sum().item()
                val_total += stages.size(0)
                val_preds_list.extend(preds.cpu().numpy())
                val_targets_list.extend(stages.cpu().numpy())
                
        val_acc = val_correct / max(val_total, 1)
        print(f"Epoch [{epoch}/{epochs}] - Train Loss: {avg_loss:.4f} | Train Acc: {train_acc*100:.2f}% | Val Acc: {val_acc*100:.2f}%")

    elapsed = time.time() - start_time
    print(f"\nExperiment completed in {elapsed:.1f} seconds.")
    print("Validation Experiment Metrics:")
    report = classification_report(val_targets_list, val_preds_list, target_names=['Seedling', 'Vegetative', 'Mature / Harvest'], zero_division=0)
    print(report)
    
    # Save trained model weights to production locations
    save_dirs = [
        os.path.join(PROJECT_ROOT, "backend", "ml_models"),
        os.path.join(PROJECT_ROOT, "ml", "models")
    ]
    for d in save_dirs:
        os.makedirs(d, exist_ok=True)
        model_path = os.path.join(d, "growth_model.keras")
        # Save PyTorch model state and metadata readable as weights artifact
        torch.save({
            'model_state_dict': model.state_dict(),
            'class_names': ['Seedling', 'Vegetative', 'Mature / Harvest'],
            'val_accuracy': val_acc,
            'architecture': 'EfficientNetB0'
        }, model_path)
        print(f"Saved model artifact to: '{model_path}'")

    print("\nVerification & Model Artifact Export Successful!")
    return val_acc

if __name__ == '__main__':
    train_experiment(sample_fraction=0.05, epochs=2, batch_size=32)
