# HydroGrow AI MLOps Pipeline Specification

The MLOps platform automates model tracking, retraining, accuracy drift monitoring, and zero-downtime model rollbacks.

---

## 1. MLOps Lifecycle Flow

```mermaid
graph LR
    Telemetry[Hardware Ingestion] --> Dataset[Training Datasets]
    Dataset --> Scheduler{TrainingScheduler Check}
    Scheduler -->|Triggers| ReFit[TrainPipeline Re-Fitting]
    ReFit --> ModelReg[ModelRegistry]
    ModelReg -->|Promote| ActiveModel[Active Production Model]
    ActiveModel --> Predict[/api/predict]
    Predict --> Log[ModelPredictionLog]
    Log --> Monitor[ModelMonitor Drift Profiling]
```

---

## 2. Automated Trigger Conditions

- **Accuracy Degradation Trigger:** Automatically triggers when model R² accuracy drops below `0.85`.
- **Data Growth Trigger:** Automatically triggers when 500+ fresh telemetry samples accumulate.
- **Rollback Protocol:** Instant 1-click version rollback available via `POST /api/ml/rollback/{id}`.
