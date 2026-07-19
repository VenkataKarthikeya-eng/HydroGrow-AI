# HydroGrow AI Frontend

React + Tailwind CSS frontend application for HydroGrow AI smart hydroponics platform.

## 🔬 Plant Doctor AI Scanner

### Features:
- Lettuce growth stage prediction
- Growth day estimation
- Nutrient deficiency detection
- AI cultivation recommendations

### Architecture:
```
React Frontend (PlantDoctor.jsx)
        ↓
FastAPI (/api/vision/plant-analysis)
        ↓
EfficientNetB0 (Model 1) + MobileNetV3Small (Model 2)
        ↓
AI Plant Report
```
