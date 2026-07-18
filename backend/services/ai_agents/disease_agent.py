class DiseaseAgent:
    """
    Autonomous sub-agent parsing Computer Vision leaf pathology diagnostic reports
    to evaluate plant pathogen risks and sanitation protocols.
    """

    @staticmethod
    def run(context: dict) -> dict:
        vision = context.get("vision_info", {})
        disease = vision.get("disease", "Healthy")
        confidence = vision.get("confidence", 0.95)
        if confidence <= 1.0:
            confidence = confidence * 100.0
        severity = vision.get("severity", "Low")
        health_score = vision.get("health_score", 98.0)

        issues = []
        recommendations = []
        priority = "LOW"
        affected_params = ["leaf_pathology"]

        if disease == "Tip Burn":
            issues.append("Tip Burn necrosis detected on lettuce leaves (Calcium transport lockout).")
            recommendations.append("Reduce Nutrient Pump EC output, lower air temperatures, and increase Calcium dosing.")
            priority = "HIGH"
            affected_params.extend(["water_ec", "temperature", "calcium"])
        elif "Root Rot" in disease:
            issues.append("Pythium Root Rot symptoms detected in root zone.")
            recommendations.append("Flush reservoir tank, apply hydrogen peroxide sanitizer, and run water chiller.")
            priority = "CRITICAL"
            affected_params.extend(["water_temperature", "root_zone"])
        elif disease == "Nutrient Deficiency":
            issues.append("Leaf chlorosis indicates macronutrient uptake lockout.")
            recommendations.append("Calibrate reservoir pH to 6.0 and replenish macro A/B solutions.")
            priority = "MEDIUM"
            affected_params.extend(["water_ph", "water_ec"])
        elif disease in ["Leaf Spot", "Fungal Stress"]:
            issues.append(f"{disease} detected on plant foliage.")
            recommendations.append("Prune affected leaves, lower ambient humidity, and activate air circulation fans.")
            priority = "HIGH"
            affected_params.extend(["humidity", "airflow"])

        if not issues:
            analysis = "No plant diseases or leaf pathology stresses detected by Computer Vision scans."
            rec_action = "Maintain regular crop health scanning schedule."
        else:
            analysis = " ".join(issues)
            rec_action = " ".join(recommendations)

        return {
            "agent_name": "DiseaseAgent",
            "decision_type": "Disease",
            "priority": priority,
            "title": "Computer Vision Plant Pathology & Disease Risk Diagnostic",
            "analysis": analysis,
            "recommended_action": rec_action,
            "confidence_score": round(confidence, 1),
            "affected_parameters": affected_params
        }
