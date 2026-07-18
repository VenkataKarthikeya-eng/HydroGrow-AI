from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.services.analytics.analytics_engine import AnalyticsEngine
from backend.services.analytics.trend_analyzer import TrendAnalyzer
from backend.services.analytics.performance_metrics import PerformanceMetrics
from backend.services.analytics.farm_report_generator import FarmReportGenerator
from backend.services.analytics.anomaly_detector import AnomalyDetector
from backend.database.models import PlantImage, PlantAnalysis
from sqlalchemy import func

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing, invalid, or expired."
        )
    return current_user

@router.get("/overview", summary="Get farm KPI overview statistics")
def get_overview(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    stats = AnalyticsEngine.get_user_statistics(db, user.id)
    metrics = PerformanceMetrics.calculate_performance_metrics(db, user.id)
    return {
        "total_cycles": stats["total_predictions"],
        "average_weight": stats["average_weight"],
        "best_prediction": stats["best_prediction"],
        "success_rate": stats["success_rate"],
        "improvement_percentage": metrics["improvement_percentage"],
        "main_issue": metrics["main_issue"]
    }

@router.get("/trends", summary="Get timeseries weight growth trends")
def get_trends(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    summary = AnalyticsEngine.get_prediction_summary(db, user.id)
    trends = TrendAnalyzer.get_parameter_trends(db, user.id)
    return {
        "weight_history": summary,
        "parameter_correlations": trends
    }

@router.get("/environment", summary="Get environmental averages and stability analysis")
def get_environment(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    return AnalyticsEngine.get_environment_statistics(db, user.id)

@router.get("/report", summary="Get AI-generated farm report")
def get_report(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    report_text = FarmReportGenerator.generate_farm_report(db, user.id)
    return {
        "report": report_text
    }

@router.get("/anomalies", summary="Get system warning and critical anomalies alerts")
def get_anomalies(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    alerts = AnomalyDetector.detect_anomalies(db, user.id)
    return {
        "anomalies": alerts
    }

@router.get("/vision", summary="Get vision analytics and trends")
def get_vision_analytics(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    scans = (
        db.query(PlantAnalysis)
        .join(PlantImage)
        .filter(PlantImage.user_id == user.id)
        .order_by(PlantAnalysis.created_at.asc())
        .all()
    )
    
    if not scans:
        return {
            "average_health_score": 0.0,
            "disease_frequency": {},
            "growth_stage_distribution": {},
            "plant_health_trends": [],
            "visual_stress_history": [],
            "latest_scan": None
        }

    avg_score = sum(s.health_score for s in scans) / len(scans)

    disease_freq = {}
    for s in scans:
        disease_freq[s.disease_name] = disease_freq.get(s.disease_name, 0) + 1

    stage_dist = {}
    for s in scans:
        stage = s.image.growth_stage
        stage_dist[stage] = stage_dist.get(stage, 0) + 1

    trends = []
    daily_groups = {}
    for s in scans:
        day_str = s.image.uploaded_at.date().isoformat() if s.image.uploaded_at else "Unknown"
        if day_str not in daily_groups:
            daily_groups[day_str] = []
        daily_groups[day_str].append(s.health_score)
        
    for day, scores in sorted(daily_groups.items()):
        trends.append({
            "date": day,
            "health_score": round(sum(scores) / len(scores), 2)
        })

    stress_history = [
        {
            "id": s.id,
            "disease": s.disease_name,
            "health_score": s.health_score,
            "severity": s.severity,
            "growth_stage": s.image.growth_stage,
            "uploaded_at": s.image.uploaded_at.isoformat() if s.image.uploaded_at else None
        }
        for s in reversed(scans)
    ]

    latest = scans[-1]
    latest_scan = {
        "id": latest.id,
        "health_score": latest.health_score,
        "disease": latest.disease_name,
        "confidence": latest.confidence_score,
        "severity": latest.severity,
        "growth_stage": latest.image.growth_stage,
        "recommendations": latest.recommendations,
        "uploaded_at": latest.image.uploaded_at.isoformat() if latest.image.uploaded_at else None
    }

    return {
        "average_health_score": round(avg_score, 2),
        "disease_frequency": disease_freq,
        "growth_stage_distribution": stage_dist,
        "plant_health_trends": trends,
        "visual_stress_history": stress_history,
        "latest_scan": latest_scan
    }
