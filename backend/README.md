# HydroGrow AI Backend — Render.com Production Deployment Guide

FastAPI AI backend powering HydroGrow AI platform, serving Crop Identity Validation (MobileNetV3), Growth Prediction (EfficientNetB0), and Nutrient Deficiency Detection (MobileNetV3) models.

---

## 🚀 Quick Render.com Deployment Options

### Option A: Web Service (Python Native)

1. Connect GitHub Repository on Render: `VenkataKarthikeya-eng/HydroGrow-AI`
2. **Runtime**: `Python 3`
3. **Build Command**:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. **Start Command**:
   ```bash
   uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
   ```
5. **Environment Variables**:
   - `API_ENV`: `production`
   - `CORS_ORIGINS`: `https://hydrogrow-ai.vercel.app,http://localhost:5173,*`

---

### Option B: Docker Container Deployment (Recommended)

1. Select **Docker** environment on Render.
2. **Dockerfile Path**: `Dockerfile` or `backend/Dockerfile`
3. Render automatically builds the container image and starts:
   ```bash
   uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
   ```

---

## 🔍 Health & AI Endpoints

- **Health Check**: `GET /health` -> `{"status": "healthy", "service": "HydroGrow AI Backend"}`
- **Crop Identity & Pathology Scanner**: `POST /api/vision/plant-analysis`
- **Growth Prediction**: `POST /api/vision/predict-growth`
- **Nutrient Deficiency Detection**: `POST /api/vision/predict-nutrient`
- **Swagger Documentation**: `GET /docs`
