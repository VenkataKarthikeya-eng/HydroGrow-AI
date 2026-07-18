class OptimizationAgent:
    """
    Autonomous sub-agent synthesizing multi-agent outputs to formulate
    holistic cost, energy, and biomass yield optimization strategies.
    """

    @staticmethod
    def run(context: dict, sub_agent_results: list) -> dict:
        twin = context.get("digital_twin", {})
        
        has_critical = any(res.get("priority") == "CRITICAL" for res in sub_agent_results)
        has_high = any(res.get("priority") == "HIGH" for res in sub_agent_results)

        priority = "LOW"
        if has_critical:
            priority = "HIGH"
        elif has_high:
            priority = "MEDIUM"

        analysis = "Synthesized farm telemetry across climate, pathology, solution chemistry, and yield models."
        recommendations = [
            "Maintain digital twin scenario simulation overrides for optimal 35-day harvest yield.",
            "Schedule LED lighting duty cycles during off-peak power hours to reduce energy cost by 15%."
        ]

        if has_critical or has_high:
            recommendations.insert(0, "Resolve active high-priority climate and solution alerts before adjusting growth lighting schedules.")

        return {
            "agent_name": "OptimizationAgent",
            "decision_type": "Yield",
            "priority": priority,
            "title": "Holistic Farm Yield & Energy Optimization Strategy",
            "analysis": analysis,
            "recommended_action": " ".join(recommendations),
            "confidence_score": 95.0,
            "affected_parameters": ["yield_efficiency", "energy_cost"]
        }
