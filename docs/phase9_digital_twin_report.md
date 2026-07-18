# Phase 9 Technical Report: Digital Twin & Crop Simulation Intelligence Engine

This report details the design and deployment of the Digital Twin smart farming capabilities inside HydroGrow AI.

---

## 1. Architecture Flow

The digital twin module replicates biological lettuce growth dynamically, mapping environmental settings and nutrient recipes over duration periods.

```mermaid
graph TD
    UI[React Digital Twin Deck] -->|POST Override parameters| Route[/api/twin/simulate]
    Route -->|Telemetry resolution| TE[Twin Engine]
    TE -->|Consume IoT/history| DB[(PostgreSQL DB)]
    Route -->|Daily loops| GS[Growth Simulator]
    GS -->|Incremental projections| FE[Forecast Engine]
    GS -->|Stresses & advice| SE[Scenario Engine]
    Route -->|Saves state log| DB
    Route -->|Pushes frames day-by-day| WS[ws_manager.broadcast_to_user]
    WS -->|Live updates stream| UI
```

---

## 2. Database Models & Relationships

Four tables were created:

```mermaid
erDiagram
    users ||--o{ digital_twin_profiles : "registers"
    users ||--o{ simulation_runs : "runs"
    digital_twin_profiles ||--o{ simulation_runs : "records"
    simulation_runs ||--o{ simulation_parameters : "defines"
    simulation_runs ||--o{ growth_forecasts : "generates"
    
    digital_twin_profiles {
        int id PK
        int user_id FK
        string farm_name
        string crop_type
        string system_type
        float area_size
        string lighting_setup
        string nutrient_system
        datetime created_at
    }

    simulation_runs {
        int id PK
        int user_id FK
        int profile_id FK
        string scenario_name
        int duration_days
        json initial_conditions
        json final_prediction
        float yield_change_percentage
        datetime created_at
    }

    simulation_parameters {
        int id PK
        int simulation_id FK
        string parameter_name
        float original_value
        float modified_value
        float impact_score
    }

    growth_forecasts {
        int id PK
        int simulation_id FK
        int day_number
        float predicted_height
        float predicted_weight
        float health_score
        string growth_stage
        datetime created_at
    }
```

---

## 3. Crop Simulation Flow

Projections compute daily increments across lettuce crop lifecycles:
1. **Seedling Stage** (Days 1–10)
2. **Vegetative Stage** (Days 11–25)
3. **Maturity Stage** (Days 26–35)
4. **Harvest Stage** (Days 35+)

Modifiers compute growth penalties relative to ideal lettuce standards (Temp: 22°C, EC: 2.0 mS, pH: 6.0):
- **Thermal Stresses**: High air temperature reduces biomass expansion and lowers crop turgidity indices.
- **Salt Stresses**: EC spikes risk leaf tip burn necrosis.

---

## 4. API Endpoints

- `POST /api/twin/create`: CRUD configuration profiles.
- `POST /api/twin/simulate`: Executes simulation cycles and broadcasts ticks over WebSocket.
- `GET /api/twin/forecast/{simulation_id}`: Returns daily forecast logs.
- `POST /api/twin/compare`: Evaluates override parameters relative to baseline indexes.
- `GET /api/twin/history`: Returns simulation run histories.
- `GET /api/twin/recommendations`: Provides AI recovery recommendations.

---

## 5. Verification Results

- Unit tests executed: **109**
- Status: **ALL PASSED (OK)**
- Production React compilation: **Clean build, 0 errors**
