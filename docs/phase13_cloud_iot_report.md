# Phase 13 Technical Report: Cloud Infrastructure, Real IoT Hardware Integration & MLOps Platform

This document presents the complete technical specification for **Phase 13 — HydroGrow AI Cloud Infrastructure, Real IoT Hardware Integration & MLOps Platform**.

---

## 1. Cloud Infrastructure & IoT Architecture

```mermaid
graph TD
    ESP32[ESP32 / Raspberry Pi Hardware Nodes] -->|MQTT Protocol / JSON| Broker[MQTT Broker]
    Broker -->|Ingestion Stream| TelemetryProc[TelemetryProcessor Pipeline]
    TelemetryProc -->|Filtered & Normalized| DB[(Managed PostgreSQL)]
    TelemetryProc -->|Live Stream| WS[/ws/iot/live WebSockets]
    WS --> Client[React Cloud Operations Deck /cloud]

    subgraph MLOps Lifecycle Platform
        Dataset[Training Datasets] --> Scheduler[TrainingScheduler Trigger]
        Scheduler --> Fitting[TrainPipeline ML Re-Fitting]
        Fitting --> Registry[ModelRegistry Version Control]
        Registry --> Monitor[ModelMonitor Accuracy & Drift Tracker]
    end
```

---

## 2. IoT Hardware Payload Format & Integration

Hardware telemetry payloads from ESP32 microcontrollers, Raspberry Pi gateways, or Arduino sensor nodes are formatted in standard JSON:

```json
{
  "device_id": "ESP32_001",
  "temperature": 24.5,
  "humidity": 68.0,
  "water_ph": 6.15,
  "water_ec": 1.85,
  "water_temperature": 22.0,
  "co2": 450.0,
  "nutrient_level": 85.0
}
```

- **Device API Authentication**: API keys generated via `POST /api/devices/register` (`hg_key_...`) and validated via `X-API-Key` SHA-256 hash lookup in `IoTDeviceCredential`.
- **Local Fallback Mode**: Automatic MQTT fallback simulation active when external brokers are unreachable.

---

## 3. MLOps Lifecycle & Automation

1. **`ModelRegistry`**: Versioning, active stage promotion, and instant single-click rollback.
2. **`TrainingScheduler`**: Automated re-training triggers when accuracy drops below 85% or dataset thresholds reach 500 samples.
3. **`ModelMonitor`**: Tracks accuracy drift, latency profiling (ms), and active inference volume.
4. **`ExperimentTracker`**: Hyperparameter tracking for Scikit-Learn regressors and pathology classifiers.

---

## 4. Verification & Testing Results

- **Backend Unit Tests:** **141 tests executed, 141 passed (OK)**.
- **Frontend Production Build:** Vite compiled production React bundle with **0 errors**.
- **Alembic Database Migration:** `01a175af9a42_add_phase_13_cloud_iot_and_mlops_tables` applied with complete rollback testing.
