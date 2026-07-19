# HydroGrow AI — Model 2: Nutrient Deficiency Detection Report

## Executive Summary
This report documents the architectural design, dataset characteristics, training methodology, and evaluation metrics for **Model 2: Lettuce Nutrient Deficiency Detection AI** built for the **HydroGrow AI** platform. The model utilizes transfer learning with **MobileNetV3Small** to classify hydroponic lettuce leaf health conditions (`Healthy`, `Nitrogen Deficiency`, `Phosphorus Deficiency`, `Potassium Deficiency`).

---

## 1. Problem Statement & Objectives

Nutrient imbalances in hydroponic lettuce cultivation cause severe yield reduction if undetected. **Model 2** enables visual leaf diagnosis:
- **Input**: High-resolution leaf image
- **Output**: Nutrient condition, confidence score, and specific cultivation recommendation

---

## 2. Dataset Description & Imbalance Analysis

- **Total Images**: **208 images** across 4 condition classes
- **Corrupted Images**: **0 files**
- **Resolution**: ~1024 × 1000 pixels (RGB)

| Class | Folder Name | Image Count | Percentage | Class Status |
| :--- | :--- | :--- | :--- | :--- |
| **Healthy** | `healthy` | 12 | 5.8% | **Severe Minority** |
| **Nitrogen Deficiency** | `nitrogen_deficiency` | 58 | 27.9% | Moderate |
| **Phosphorus Deficiency** | `phosphorus_deficiency` | 66 | 31.7% | Moderate |
| **Potassium Deficiency** | `potassium_deficiency` | 72 | 34.6% | **Majority Class** |
| **Total** | | **208** | **100.0%** | |

### Imbalance Mitigation Strategy
1. **Stratified Split**: 70% Training (145 images), 20% Validation (42 images), 10% Testing (21 images).
2. **Minority Augmentation**: Applied heavy random rotation (±30°), flips, zoom (±20%), brightness and contrast jitter specifically to the 12 `healthy` class images.
3. **Class Weighting**: Weighted CrossEntropyLoss inverse to class frequency (`healthy` weight: 4.03x).

---

## 3. Model Architecture & Training Methodology

### Network Architecture
- **Backbone**: MobileNetV3Small (Pre-trained on ImageNet)
- **Input Shape**: 224 × 224 × 3
- **Feature Pooling**: Global Average Pooling
- **Classification Head**: Dense(256) -> Hardswish -> Dropout(0.3) -> Dense(4, Softmax)

```
                    Leaf Image (224x224)
                             │
               Data Augmentation & Normalization
                             │
               MobileNetV3Small Feature Extractor
                             │
                   Global Average Pooling
                             │
                Dense Classifier & Softmax
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
       Predicted Condition          Confidence & Advice
   (Healthy / N / P / K Def)    ("Increase nitrogen supply...")
```

### Hyperparameters & Optimization
- **Optimizer**: Adam (learning rate = 1e-3, weight decay = 1e-4)
- **Loss Function**: Weighted Cross-Entropy Loss
- **Learning Rate Scheduler**: `ReduceLROnPlateau` (factor = 0.5, patience = 3)

---

## 4. Actual Performance & Evaluation Metrics

### Training & Validation Loss Curves
- **Peak Validation Accuracy**: **95.2%** (Epoch 14, Val Loss: 0.0968)
- **Final Test Accuracy**: **85.71%** (21 Test Images)

### Per-Class Precision, Recall, and F1-Score (Test Set)
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| **Healthy** | 1.00 | 1.00 | 1.00 | 1 |
| **Nitrogen Deficiency** | 0.67 | 1.00 | 0.80 | 6 |
| **Phosphorus Deficiency** | 1.00 | 1.00 | 1.00 | 7 |
| **Potassium Deficiency** | 1.00 | 0.57 | 0.73 | 7 |
| **Macro Average** | **0.92** | **0.89** | **0.88** | **21** |
| **Weighted Average** | **0.90** | **0.86** | **0.85** | **21** |

### Actual Confusion Matrix
```
                  Predicted
              H   N   P   K
Actual  H    [1   0   0   0]
        N    [0   6   0   0]
        P    [0   0   7   0]
        K    [0   3   0   4]
```


---

## 5. API & Backend Services

### Individual Endpoint: `POST /api/vision/predict-nutrient`
Returns condition, confidence score, and specific recommendation:
```json
{
  "condition": "Nitrogen Deficiency",
  "confidence": 0.91,
  "recommendation": "Increase nitrogen concentration and monitor chlorosis."
}
```

### Combined Endpoint: `POST /api/vision/plant-analysis`
Combines Model 1 (Growth) and Model 2 (Nutrient) into unified JSON:
```json
{
  "growth_prediction": {
    "stage": "Vegetative",
    "growth_day": 18,
    "confidence": 0.94
  },
  "nutrient_prediction": {
    "condition": "Healthy",
    "confidence": 0.92
  },
  "recommendation": "Plant growth is normal. Maintain nutrient schedule."
}
```

---

## 6. Limitations & Future Work

### Limitations
1. **Small Sample Size**: The `healthy` class contains only 12 images. Test set sample size for healthy is small (2 images).
2. **Single Deficiency**: Leaf samples exhibiting multiple concurrent nutrient deficiencies are classified into the primary dominant deficiency.

### Future Work
1. **Data Expansion**: Collect additional high-resolution images for healthy hydroponic lettuce under varying LED lighting.
2. **Edge Quantization**: Export MobileNetV3Small model to TFLite format for on-device inference on farm micro-controllers.
