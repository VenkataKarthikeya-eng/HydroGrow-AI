import os
import sys
import time
import ssl
import glob
import pandas as pd
import numpy as np
from PIL import Image

# Bypass SSL cert verification for PyTorch hub weights download
ssl._create_default_https_context = ssl._create_unverified_context

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as T
import torchvision.models as models
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.utils.class_weight import compute_class_weight

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

CLASS_NAMES = ['healthy', 'nitrogen_deficiency', 'phosphorus_deficiency', 'potassium_deficiency']
CLASS_TO_IDX = {c: i for i, c in enumerate(CLASS_NAMES)}
IDX_TO_CLASS = {i: c for i, c in enumerate(CLASS_NAMES)}

class NutrientDataset(Dataset):
    def __init__(self, df, transform=None, is_minority_aug=False):
        self.df = df.reset_index(drop=True)
        self.transform = transform
        self.is_minority_aug = is_minority_aug
        
        # Stronger augmentation for healthy class
        self.healthy_extra_transform = T.Compose([
            T.Resize((224, 224)),
            T.RandomHorizontalFlip(p=0.8),
            T.RandomVerticalFlip(p=0.5),
            T.RandomRotation(30),
            T.ColorJitter(brightness=0.2, contrast=0.2),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

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
            image = Image.new('RGB', (224, 224), (0, 0, 0))

        label_idx = CLASS_TO_IDX[row['class']]
        
        # Apply stronger augmentation if healthy class
        if self.is_minority_aug and row['class'] == 'healthy':
            image = self.healthy_extra_transform(image)
        elif self.transform:
            image = self.transform(image)
            
        return image, torch.tensor(label_idx, dtype=torch.long)

class MobileNetV3NutrientModel(nn.Module):
    def __init__(self, num_classes=4):
        super().__init__()
        weights = models.MobileNet_V3_Small_Weights.DEFAULT
        self.backbone = models.mobilenet_v3_small(weights=weights)
        in_features = self.backbone.classifier[0].in_features
        
        # Replace classifier head
        self.backbone.classifier = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.Hardswish(),
            nn.Dropout(p=0.3),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        return self.backbone(x)

def train_nutrient_model(epochs=15, batch_size=16):
    print("=" * 60)
    print("STEPS 2-4: MOBILENETV3-SMALL NUTRIENT DEFICIENCY MODEL TRAINING")
    print("=" * 60)
    
    dataset_dir = os.path.join(PROJECT_ROOT, "data", "nutrient_dataset")
    records = []
    for cls in CLASS_NAMES:
        cls_dir = os.path.join(dataset_dir, cls)
        for img_p in glob.glob(os.path.join(cls_dir, "*.*")):
            ext = os.path.splitext(img_p)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg']:
                records.append({
                    'image_path': os.path.normpath(img_p).replace('\\', '/'),
                    'class': cls
                })
                
    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} total images from dataset.")
    
    # Stratified 70% Train, 20% Val, 10% Test split
    train_val_df, test_df = train_test_split(df, test_size=0.10, stratify=df['class'], random_state=42)
    train_df, val_df = train_test_split(train_val_df, test_size=2/9, stratify=train_val_df['class'], random_state=42) # 2/9 of 90% is 20%
    
    print(f"Dataset Split: Train={len(train_df)} | Val={len(val_df)} | Test={len(test_df)}")
    
    # Compute class weights for loss function
    train_labels = [CLASS_TO_IDX[c] for c in train_df['class']]
    class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(train_labels), y=train_labels)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    weights_tensor = torch.tensor(class_weights, dtype=torch.float32).to(device)
    print(f"Calculated Class Weights for Loss: {dict(zip(CLASS_NAMES, class_weights.round(2)))}")

    # Standard Augmentation & Transforms
    train_transform = T.Compose([
        T.Resize((224, 224)),
        T.RandomHorizontalFlip(),
        T.RandomRotation(20),
        T.ColorJitter(brightness=0.15, contrast=0.15),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    val_test_transform = T.Compose([
        T.Resize((224, 224)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_loader = DataLoader(NutrientDataset(train_df, train_transform, is_minority_aug=True), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(NutrientDataset(val_df, val_test_transform), batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(NutrientDataset(test_df, val_test_transform), batch_size=batch_size, shuffle=False)

    model = MobileNetV3NutrientModel(num_classes=4).to(device)
    criterion = nn.CrossEntropyLoss(weight=weights_tensor)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)

    best_val_loss = float('inf')
    best_model_state = None

    print(f"\nTraining MobileNetV3Small on {device}...")
    for epoch in range(1, epochs + 1):
        model.train()
        train_loss, train_correct, train_total = 0.0, 0, 0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * imgs.size(0)
            preds = torch.argmax(outputs, dim=1)
            train_correct += (preds == labels).sum().item()
            train_total += labels.size(0)

        epoch_train_loss = train_loss / train_total
        epoch_train_acc = train_correct / train_total

        # Validation phase
        model.eval()
        val_loss, val_correct, val_total = 0.0, 0, 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                outputs = model(imgs)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * imgs.size(0)
                preds = torch.argmax(outputs, dim=1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)

        epoch_val_loss = val_loss / val_total
        epoch_val_acc = val_correct / val_total
        scheduler.step(epoch_val_loss)

        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            best_model_state = model.state_dict().copy()

        print(f"Epoch [{epoch:02d}/{epochs}] - Train Loss: {epoch_train_loss:.4f} Acc: {epoch_train_acc*100:.1f}% | Val Loss: {epoch_val_loss:.4f} Acc: {epoch_val_acc*100:.1f}%")

    # Load best model for testing & evaluation
    model.load_state_dict(best_model_state)
    model.eval()
    
    test_preds, test_targets = [], []
    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs = imgs.to(device)
            outputs = model(imgs)
            preds = torch.argmax(outputs, dim=1)
            test_preds.extend(preds.cpu().numpy())
            test_targets.extend(labels.numpy())

    test_acc = accuracy_score(test_targets, test_preds)
    print(f"\nFinal Test Accuracy: {test_acc * 100:.2f}%")
    print("\nClassification Report (Per-Class Precision, Recall, F1):")
    report = classification_report(test_targets, test_preds, target_names=CLASS_NAMES, zero_division=0)
    print(report)

    cm = confusion_matrix(test_targets, test_preds)
    print("Confusion Matrix:")
    print(cm)

    # Save trained model to backend/ml_models/nutrient_model.keras and ml/models/nutrient_model.keras
    save_dirs = [
        os.path.join(PROJECT_ROOT, "backend", "ml_models"),
        os.path.join(PROJECT_ROOT, "ml", "models")
    ]
    
    artifact_payload = {
        'model_state_dict': best_model_state,
        'class_names': CLASS_NAMES,
        'test_accuracy': float(test_acc),
        'architecture': 'MobileNetV3Small'
    }

    for d in save_dirs:
        os.makedirs(d, exist_ok=True)
        model_path = os.path.join(d, "nutrient_model.keras")
        torch.save(artifact_payload, model_path)
        print(f"Saved model artifact to '{model_path}'")

    print("\nNutrient Model Training & Export Completed Successfully!")
    return test_acc

if __name__ == '__main__':
    train_nutrient_model(epochs=15, batch_size=16)
