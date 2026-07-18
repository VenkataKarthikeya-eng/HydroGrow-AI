# HydroGrow AI System Architecture Overview

HydroGrow AI is an enterprise autonomous smart farming platform engineered across 12 modular phases.

---

## High-Level Architecture Diagram

```mermaid
graph TD
    User[Farmer / User Deck] --> UI[Vite React Frontend SPA]
    UI -->|REST & WebSockets| API[FastAPI Application Server]

    subgraph Security & Core
        API --> Auth[JWT Authentication Handler]
        API --> SecMiddleware[Security Headers & Logger]
        API --> Settings[Settings & Config Loader]
    end

    subgraph Intelligence Systems
        API --> ML[MLEngine Scikit-Learn Regressor & Classifiers]
        API --> Copilot[DecisionEngine & Multi-Agent Harvester]
        API --> Vision[Computer Vision Pathology Analyzer]
        API --> Twin[Digital Twin Scenario Simulator]
        API --> RAG[AI Assistant & RAG Vector Memory]
        API --> Automation[Smart Automation Relay Engine]
    end

    subgraph Persistence & Monitoring
        API --> DB[(PostgreSQL Database)]
        API --> Backup[BackupManager PG Dumps]
        API --> SystemRoutes[Health & System Monitor]
    end
```

---

## Subsystem Matrix

| Subsystem | Components | Primary Responsibilities |
| :--- | :--- | :--- |
| **Growth Prediction** | `prediction.py`, `growth_model.py` | Biomass weight prediction (g), validation clipping, and R² metrics |
| **IoT Telemetry** | `sensor_manager.py`, `/ws/iot/live` | Live sensor data ingestion, boundary validation, WebSocket streaming |
| **Automation Engine** | `crop_lifecycle_manager.py`, `action_simulator.py` | Actuator simulation (fans, nutrient pumps, pH dosing, chillers) |
| **Computer Vision** | `image_processor.py`, `disease_detector.py` | Leaf pathology diagnosis (Tip Burn, Root Rot, Chlorosis) |
| **Digital Twin** | `growth_simulator.py`, `scenario_engine.py` | 35-day virtual crop growth simulation & override comparisons |
| **Autonomous Copilot**| `decision_engine.py`, 5 AI Sub-Agents | Multi-agent context harvester, deduplication, priority ranking |
| **Machine Learning** | `ml_engine.py`, `train_pipeline.py` | RandomForest models, model version control, zero-crash fallback |
| **Production Core** | `backup_manager.py`, `security.py` | Database backups, security headers, container health checks |
