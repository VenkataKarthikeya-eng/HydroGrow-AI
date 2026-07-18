# HydroGrow AI Cloud Architecture Specification

HydroGrow AI cloud infrastructure is designed for cloud-agnostic deployment across AWS, Azure, Google Cloud, and Kubernetes.

---

## 1. Cloud Infrastructure Matrix

| Cloud Layer | Service / Technology | Fallback / Alternative |
| :--- | :--- | :--- |
| **API Backend** | FastAPI / Docker Container (port 8000) | Uvicorn / Gunicorn |
| **Frontend SPA** | React Vite Static Bundle / Nginx (port 80) | S3 Static Hosting / Cloudflare Pages |
| **Database** | Managed PostgreSQL (RDS / Cloud SQL) | Local PostgreSQL Container |
| **Cloud Storage** | AWS S3 / Azure Blob / Google Cloud Storage | Local Filesystem (`uploads/`) |
| **IoT Transport** | MQTT Broker (EMQX / Mosquitto) | HTTP Telemetry Fallback |
| **Orchestration** | Kubernetes (`deployment/`) | Docker Compose |
