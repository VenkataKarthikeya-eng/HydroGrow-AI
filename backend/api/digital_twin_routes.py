import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import DigitalTwinProfile, SimulationRun, SimulationParameters, GrowthForecast
from backend.services.digital_twin.twin_engine import TwinEngine
from backend.services.digital_twin.forecast_engine import ForecastEngine
from backend.services.digital_twin.scenario_engine import ScenarioEngine
from backend.services.digital_twin.optimization_strategy import OptimizationStrategy
from backend.api.websocket_routes import ws_manager

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

class ProfileCreate(BaseModel):
    farm_name: str = Field(..., min_length=2, max_length=50)
    system_type: str = Field(default="NFT Hydroponics")
    area_size: float = Field(default=20.0)
    lighting_setup: str = Field(default="LED Lighting")
    nutrient_system: str = Field(default="Auto Nutrient Pump")

class SimulationInput(BaseModel):
    scenario_name: str = Field(..., min_length=2, max_length=50)
    duration_days: int = Field(default=35, ge=5, le=60)
    overrides: Dict[str, float] = Field(default={})

class CompareInput(BaseModel):
    original_conditions: Dict[str, float] = Field(default={})
    modified_conditions: Dict[str, float] = Field(default={})
    duration_days: int = Field(default=35)

@router.post("/create", summary="Register or update digital twin profile")
def create_profile(
    data: ProfileCreate, 
    db: Session = Depends(get_db), 
    user: Any = Depends(get_current_user_required)
):
    profile = TwinEngine.create_virtual_profile(
        db, 
        user_id=user.id,
        farm_name=data.farm_name,
        system_type=data.system_type,
        area_size=data.area_size,
        lighting_setup=data.lighting_setup,
        nutrient_system=data.nutrient_system
    )
    return {
        "id": profile.id,
        "farm_name": profile.farm_name,
        "crop_type": profile.crop_type,
        "system_type": profile.system_type,
        "area_size": profile.area_size,
        "lighting_setup": profile.lighting_setup,
        "nutrient_system": profile.nutrient_system
    }

@router.post("/simulate", summary="Trigger crop growth simulation loop")
async def run_simulation(
    data: SimulationInput, 
    db: Session = Depends(get_db), 
    user: Any = Depends(get_current_user_required)
):
    # 1. Resolve Profile
    profile = db.query(DigitalTwinProfile).filter(DigitalTwinProfile.user_id == user.id).first()
    if not profile:
        profile = TwinEngine.create_virtual_profile(
            db, 
            user_id=user.id,
            farm_name="Default Twin Farm",
            system_type="NFT Hydroponics",
            area_size=20.0,
            lighting_setup="LED Lighting",
            nutrient_system="Auto Nutrient Pump"
        )

    # 2. Compile Baseline
    baseline = TwinEngine.resolve_farm_baseline_conditions(db, user.id)
    
    # 3. Apply Overrides
    modified = {**baseline, **data.overrides}

    # 4. Scenario comparisons
    comparison = ScenarioEngine.run_scenario_comparison(baseline, modified, data.duration_days)

    # 5. Generate forecasts
    forecast_data = ForecastEngine.generate_growth_forecast(modified, data.duration_days)

    # 6. Save Simulation Run
    final_pred = {
        "weight": forecast_data["expected_harvest_weight"],
        "height": forecast_data["growth_forecast"][-1]["predicted_height"],
        "health": forecast_data["growth_forecast"][-1]["health_score"]
    }
    
    run = SimulationRun(
        user_id=user.id,
        profile_id=profile.id,
        scenario_name=data.scenario_name,
        duration_days=data.duration_days,
        initial_conditions=modified,
        final_prediction=final_pred,
        yield_change_percentage=comparison["yield_change_percentage"]
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    # 7. Save Parameters Impact
    for param_key, mod_val in data.overrides.items():
        orig_val = baseline.get(param_key, mod_val)
        param_item = SimulationParameters(
            simulation_id=run.id,
            parameter_name=param_key,
            original_value=float(orig_val),
            modified_value=float(mod_val),
            impact_score=comparison["yield_change_percentage"]
        )
        db.add(param_item)

    # 8. Save Forecast Days & stream live progress frames via WebSockets
    for day_state in forecast_data["growth_forecast"]:
        fc = GrowthForecast(
            simulation_id=run.id,
            day_number=day_state["day"],
            predicted_height=day_state["predicted_height"],
            predicted_weight=day_state["predicted_weight"],
            health_score=day_state["health_score"],
            growth_stage=day_state["growth_stage"]
        )
        db.add(fc)
        
        # Async WebSocket stream push
        ws_payload = {
            "type": "digital_twin_progress",
            "simulation_id": run.id,
            "day": day_state["day"],
            "growth_stage": day_state["growth_stage"],
            "weight": day_state["predicted_weight"],
            "health_score": day_state["health_score"]
        }
        await ws_manager.broadcast_to_user(user.id, ws_payload)
        await asyncio.sleep(0.01) # fast simulation tick

    db.commit()

    return {
        "simulation_id": run.id,
        "scenario_name": run.scenario_name,
        "yield_change_percentage": run.yield_change_percentage,
        "final_prediction": final_pred,
        "harvest_prediction": {
            "expected_weight": forecast_data["expected_harvest_weight"],
            "expected_date": forecast_data["expected_harvest_date"],
            "confidence_score": forecast_data["confidence_score"]
        },
        "recommendations": comparison["recommendations"],
        "risk_factors": forecast_data["risk_factors"]
    }

@router.get("/forecast/{simulation_id}", summary="Get forecast timeline details")
def get_forecast(
    simulation_id: int, 
    db: Session = Depends(get_db), 
    user: Any = Depends(get_current_user_required)
):
    run = db.query(SimulationRun).filter(SimulationRun.id == simulation_id, SimulationRun.user_id == user.id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Simulation run not found.")

    forecasts = db.query(GrowthForecast).filter(GrowthForecast.simulation_id == simulation_id).order_by(GrowthForecast.day_number.asc()).all()
    
    return [
        {
            "day": f.day_number,
            "predicted_height": f.predicted_height,
            "predicted_weight": f.predicted_weight,
            "health_score": f.health_score,
            "growth_stage": f.growth_stage
        }
        for f in forecasts
    ]

@router.post("/compare", summary="Compare two conditions sets")
def compare_scenarios(
    data: CompareInput, 
    db: Session = Depends(get_db), 
    user: Any = Depends(get_current_user_required)
):
    baseline = data.original_conditions if data.original_conditions else TwinEngine.resolve_farm_baseline_conditions(db, user.id)
    comparison = ScenarioEngine.run_scenario_comparison(baseline, data.modified_conditions, data.duration_days)
    return comparison

@router.get("/history", summary="List previous simulation runs")
def get_history(db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    runs = db.query(SimulationRun).filter(SimulationRun.user_id == user.id).order_by(SimulationRun.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "scenario_name": r.scenario_name,
            "duration_days": r.duration_days,
            "yield_change_percentage": r.yield_change_percentage,
            "final_weight": r.final_prediction.get("weight", 0.0),
            "final_health": r.final_prediction.get("health", 100.0),
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in runs
    ]

@router.get("/recommendations", summary="Get AI optimization tips")
def get_recommendations(db: Session = Depends(get_db), user: Any = Depends(get_current_user_required)):
    baseline = TwinEngine.resolve_farm_baseline_conditions(db, user.id)
    tips = OptimizationStrategy.formulate_strategies(baseline)
    return tips
