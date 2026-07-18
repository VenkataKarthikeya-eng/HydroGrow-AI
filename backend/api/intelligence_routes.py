from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.services.global_intelligence.farm_intelligence_engine import FarmIntelligenceEngine
from backend.services.global_intelligence.profitability_engine import ProfitabilityEngine
from backend.services.global_intelligence.market_prediction_engine import MarketPredictionEngine
from backend.services.global_intelligence.strategy_engine import StrategyEngine
from backend.services.farm_management.permission_manager import PermissionManager

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

@router.get("/intelligence/farm-score/{farm_id}", summary="Get AI farm performance intelligence score")
def get_farm_score(
    farm_id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    if not PermissionManager.has_permission(db, farm_id, user.id, "VIEWER"):
        raise HTTPException(status_code=403, detail="Access denied to this farm.")

    score_data = FarmIntelligenceEngine.calculate_farm_score(db, farm_id)
    insights = FarmIntelligenceEngine.generate_farm_insights(db, farm_id)
    bottlenecks = FarmIntelligenceEngine.detect_productivity_bottlenecks(db, farm_id)
    comparison = FarmIntelligenceEngine.compare_farm_performance(db, farm_id)

    return {
        "score": score_data,
        "insights": insights,
        "bottlenecks": bottlenecks,
        "comparison": comparison
    }

@router.get("/intelligence/profit-analysis/{farm_id}", summary="Get crop profitability forecast")
def get_profit_analysis(
    farm_id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    if not PermissionManager.has_permission(db, farm_id, user.id, "VIEWER"):
        raise HTTPException(status_code=403, detail="Access denied to this farm.")

    profit = ProfitabilityEngine.calculate_crop_profit(db, farm_id)
    comparison = ProfitabilityEngine.compare_crop_profitability(db, farm_id)
    recommendation = ProfitabilityEngine.recommend_profitable_crop(db, farm_id)

    return {
        "current_crop": profit,
        "crop_comparison": comparison,
        "top_recommendation": recommendation
    }

@router.get("/intelligence/market-trends", summary="Get regional agricultural market intelligence")
def get_market_trends(db: Session = Depends(get_db)):
    report = MarketPredictionEngine.generate_market_report(db)
    opportunities = MarketPredictionEngine.detect_market_opportunities(db)
    return {
        "market_report": report,
        "opportunities": opportunities
    }

@router.get("/intelligence/strategy/{farm_id}", summary="Get AI farm strategy plan")
def get_farm_strategy(
    farm_id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    if not PermissionManager.has_permission(db, farm_id, user.id, "VIEWER"):
        raise HTTPException(status_code=403, detail="Access denied to this farm.")

    strategies = StrategyEngine.generate_strategy(db, farm_id)
    ranked = StrategyEngine.rank_strategies(strategies)
    evaluation = StrategyEngine.evaluate_strategy_results(db, farm_id)

    return {
        "strategies": ranked,
        "evaluation": evaluation
    }

@router.post("/intelligence/generate-plan/{farm_id}", summary="Generate new 6-month autonomous farm plan")
def generate_strategy_plan(
    farm_id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    if not PermissionManager.has_permission(db, farm_id, user.id, "MANAGER"):
        raise HTTPException(status_code=403, detail="Manager permission required to generate strategy.")

    strategies = StrategyEngine.generate_strategy(db, farm_id)
    return {
        "message": "New 6-Month Autonomous Strategy Plan generated.",
        "strategies_count": len(strategies),
        "status": "Active Deployment"
    }
