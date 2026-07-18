# HydroGrow AI Deployment Guide

This guide provides step-by-step instructions for deploying HydroGrow AI in production environments.

---

## 1. Quickstart Docker Compose Deployment (Recommended)

### Prerequisites
- Docker Engine 20.10+
- Docker Compose v2+

### Step-by-Step Instructions

1. **Clone the Repository & Environment Setup:**
   ```bash
   git clone https://github.com/VenkataKarthikeya-eng/HydroGrow-AI.git
   cd HydroGrow-AI
   cp .env.example .env
   ```

2. **Configure Production Environment Variables:**
   Edit `.env` and configure secure values:
   ```env
   POSTGRES_USER=hydrogrow_prod
   POSTGRES_PASSWORD=your_secure_random_password_here
   POSTGRES_DB=hydrogrow_db
   JWT_SECRET_KEY=your_secure_jwt_secret_key_here
   API_ENV=production
   ```

3. **Build and Launch Container Stack:**
   ```bash
   docker compose up --build -d
   ```

4. **Verify Deployment Health:**
   ```bash
   curl http://localhost/health
   ```
   *Expected Response:* `{"status": "healthy", "database": "connected", "version": "1.0"}`

---

## 2. Manual Production Deployment

### Backend Setup (FastAPI & PostgreSQL)
1. Install Python 3.11+ and PostgreSQL 15+.
2. Create database and user:
   ```sql
   CREATE DATABASE hydrogrow_db;
   CREATE USER hydrogrow_prod WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE hydrogrow_db TO hydrogrow_prod;
   ```
3. Install dependencies and apply migrations:
   ```bash
   pip install -r requirements.txt
   python -m alembic upgrade head
   ```
4. Start server:
   ```bash
   uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Frontend Setup (React & Nginx)
1. Build production static bundle:
   ```bash
   cd frontend
   npm ci
   npm run build
   ```
2. Copy `frontend/dist` directory to your Nginx document root.

---

## 3. Database Maintenance & Backups

To trigger an automated database backup manually:
```bash
python -c "from backend.database.backup_manager import BackupManager; print(BackupManager().generate_backup())"
```
Backups are saved to `backups/hydrogrow_backup_YYYYMMDD_HHMMSS.sql`.
