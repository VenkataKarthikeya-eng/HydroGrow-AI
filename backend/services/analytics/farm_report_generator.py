from sqlalchemy.orm import Session
from backend.services.analytics.performance_metrics import PerformanceMetrics
from backend.services.analytics.analytics_engine import AnalyticsEngine
from backend.services.intelligence.response_formatter import ResponseFormatter

class FarmReportGenerator:
    """
    Assembles natural language agricultural performance summaries, positive factors,
    environmental problems, and actionable farm recommendations.
    """
    @staticmethod
    def generate_farm_report(db: Session, user_id: int) -> str:
        stats = AnalyticsEngine.get_user_statistics(db, user_id)
        metrics = PerformanceMetrics.calculate_performance_metrics(db, user_id)
        
        if stats["total_predictions"] == 0:
            return (
                "### HydroGrow AI Farm Report\n\n"
                "🌱 **Analysis:**\n"
                "No harvest cycles recorded yet. Complete lettuce predictions on the dashboard to generate farm insights.\n\n"
                "📊 **Evidence:**\n"
                "Total logged cycles: 0\n\n"
                "💡 **Recommendation:**\n"
                "Run environmental and water parameter inputs through the prediction panel to start logging growth cycles."
            )

        avg_weight = metrics["average_yield"]
        success = metrics["growth_success"]
        issue = metrics["main_issue"]

        analysis = f"Average lettuce harvest weight is {avg_weight} across {stats['total_predictions']} growth cycles, achieving a growth success rate of {success}."
        
        positives = []
        if "pH" not in issue:
            positives.append("Stable water pH management")
        if "EC" not in issue:
            positives.append("Balanced electrical conductivity (EC) concentrations")
        if "Temp" not in issue:
            positives.append("Healthy grow room temperatures")
            
        if not positives:
            positives.append("General seedling starting size compliance")

        evidence = "Positive Factors:\n" + "\n".join(f"- {p}" for p in positives)
        if issue != "None detected":
            evidence += f"\n\nIssues Identified:\n- {issue} detected in multiple cycles."

        recs = []
        if "EC" in issue:
            recs.append("Reduce nutrient dosing concentrations by 10% and test electrical conductivity daily.")
        elif "pH" in issue:
            recs.append("Improve pH stabilizer dosing schedules and check probe calibration weekly.")
        elif "Temp" in issue:
            recs.append("Increase ventilation extraction rates or adjust grow room AC setpoints.")
        else:
            recs.append("Maintain optimal daily parameter tracking protocols.")

        recommendations = "\n".join(f"{idx}. {r}" for idx, r in enumerate(recs, 1))

        return ResponseFormatter.format_general_response(
            title="HydroGrow AI Farm Report",
            analysis=analysis,
            evidence=evidence,
            recommendations=recommendations
        )
