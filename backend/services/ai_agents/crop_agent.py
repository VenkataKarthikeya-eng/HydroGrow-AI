class CropAgent:
    """
    Autonomous sub-agent analyzing crop lifecycle status, biomass expansion rates,
    and growth stage bottlenecks.
    """

    @staticmethod
    def run(context: dict) -> dict:
        crop_info = context.get("crop_info", {})
        forecasts = context.get("digital_twin", {}).get("forecasts", [])
        vision = context.get("vision_info", {})
        
        current_stage = crop_info.get("current_stage", "Vegetative")
        growth_progress = crop_info.get("growth_progress", 50.0)
        days_remaining = crop_info.get("days_remaining", 15)
        health_score = vision.get("health_score", 95.0)

        issues = []
        recommendations = []
        confidence = 92.0
        priority = "LOW"
        affected_params = ["growth_stage", "biomass_rate"]

        if growth_progress < 40.0 and current_stage in ["Maturity", "Harvest"]:
            issues.append("Slow growth detected relative to expected harvest date.")
            recommendations.append("Increase light exposure duration to 18 hours/day and boost nutrient solution EC by 10%.")
            priority = "HIGH"
            affected_params.extend(["light_hours", "water_ec"])
            confidence = 88.0
        elif health_score < 70.0:
            issues.append("Vegetative canopy vigor is depressed.")
            recommendations.append("Inspect flow channels for nutrient stagnation and supplement foliage aeration.")
            priority = "MEDIUM"
            affected_params.append("canopy_vigor")
            confidence = 90.0

        if not issues:
            analysis = f"Crop lifecycle is progressing optimally in the {current_stage} stage ({growth_progress}% complete)."
            rec_action = "Maintain current daily lighting and replenishment schedule."
        else:
            analysis = " ".join(issues)
            rec_action = " ".join(recommendations)

        return {
            "agent_name": "CropAgent",
            "decision_type": "Yield",
            "priority": priority,
            "title": "Crop Growth Status & Lifecycle Analysis",
            "analysis": analysis,
            "recommended_action": rec_action,
            "confidence_score": confidence,
            "affected_parameters": affected_params
        }
