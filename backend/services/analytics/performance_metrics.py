from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.database.models import Prediction

class PerformanceMetrics:
    """
    Calculates operational farm statistics including average yields,
    success rates, improvements, and recurrent bottleneck parameters.
    """
    @staticmethod
    def calculate_performance_metrics(db: Session, user_id: int) -> Dict[str, Any]:
        predictions = (
            db.query(Prediction)
            .filter(Prediction.user_id == user_id)
            .order_by(Prediction.created_at.asc())
            .all()
        )
        if not predictions:
            return {
                "average_yield": "0.0g",
                "growth_success": "0%",
                "main_issue": "No cycles recorded",
                "best_cycles": [],
                "improvement_percentage": "0.0%"
            }

        total_count = len(predictions)
        weights = [p.predicted_weight for p in predictions]
        avg_yield = sum(weights) / total_count
        
        successful_count = sum(1 for p in predictions if p.growth_category != "Poor")
        success_pct = (successful_count / total_count) * 100.0

        improvement_pct = 0.0
        if total_count >= 2:
            first_run = weights[0]
            last_run = weights[-1]
            if first_run > 0:
                improvement_pct = ((last_run - first_run) / first_run) * 100.0

        issue_counts = {}
        for p in predictions:
            recs = p.recommendations or []
            for r in recs:
                if isinstance(r, dict) and r.get("status") in ["Critical", "Warning"]:
                    param = r.get("parameter", "Unknown")
                    issue_counts[param] = issue_counts.get(param, 0) + 1

        main_issue = "None detected"
        if issue_counts:
            top_param = max(issue_counts, key=issue_counts.get)
            main_issue = f"High {top_param}" if "pH" not in top_param and "EC" not in top_param else top_param

        best_sorted = sorted(predictions, key=lambda p: p.predicted_weight, reverse=True)[:3]
        best_cycles = [
            {
                "id": p.id,
                "weight": round(p.predicted_weight, 1),
                "category": p.growth_category,
                "date": p.created_at.strftime("%Y-%m-%d") if p.created_at else "N/A"
            }
            for p in best_sorted
        ]

        return {
            "average_yield": f"{round(avg_yield, 1)}g",
            "growth_success": f"{round(success_pct, 1)}%",
            "main_issue": main_issue,
            "best_cycles": best_cycles,
            "improvement_percentage": f"{round(improvement_pct, 1)}%"
        }
