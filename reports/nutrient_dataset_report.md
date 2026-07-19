# HydroGrow AI — Nutrient Dataset Analysis Report

## Executive Summary
This report summarizes the exploratory dataset analysis performed on `data/nutrient_dataset/` for **Model 2: Lettuce Nutrient Deficiency Detection AI**.

---

## 1. Dataset Overview

- **Total Images Analyzed**: **208 images**
- **Corrupted Images**: **0 files**
- **Resolution**: High-resolution RGB images (~1024 × 1000 pixels)
- **Format**: JPG / PNG

---

## 2. Class Distribution & Imbalance Analysis

| Class Name | Image Count | Percentage | Class Status |
| :--- | :--- | :--- | :--- |
| `healthy` | 12 | 5.8% | **Severe Minority** |
| `nitrogen_deficiency` | 58 | 27.9% | Moderate |
| `phosphorus_deficiency` | 66 | 31.7% | Moderate |
| `potassium_deficiency` | 72 | 34.6% | **Majority Class** |
| **Total** | **208** | **100.0%** | — |

```
Class Distribution:
potassium_deficiency   ████████████████████ 72 (34.6%)
phosphorus_deficiency  ██████████████████   66 (31.7%)
nitrogen_deficiency    ████████████████     58 (27.9%)
healthy                ██                   12 (5.8%)
```

### Key Insights & Imbalance Ratio
- **Imbalance Ratio**: **6.00x** ratio between `potassium_deficiency` (72) and `healthy` (12).
- **Minority Class Bottleneck**: The `healthy` class contains only 12 images. Standard unweighted training could cause the model to under-predict healthy leaves.

---

## 3. Data Preprocessing & Augmentation Strategy

To resolve class imbalance and small dataset size, the training pipeline incorporates:
1. **Targeted Minority Augmentation**: Stronger random rotations (±30°), flips, zoom (±20%), brightness adjustments, and contrast jitter applied specifically to the `healthy` class.
2. **Stratified Split**: 70% Training (145 images), 20% Validation (42 images), 10% Testing (21 images) guaranteeing balanced class representation across all splits.
3. **Class Weighting**: Loss function inverse-frequency weighting to ensure minority class errors carry higher penalty during backpropagation.
4. **Primary Architecture Selection**: **MobileNetV3Small** chosen as transfer learning backbone to prevent overfitting on 208 images while enabling fast inference.
