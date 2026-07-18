class NutritionAgent:
    """
    Autonomous sub-agent analyzing hydroponic solution EC, pH drift,
    and macronutrient absorption.
    """

    @staticmethod
    def run(context: dict) -> dict:
        iot = context.get("iot_info", {})
        ph = iot.get("water_ph", 6.2)
        ec = iot.get("water_ec", 2.0)
        nutrient_level = iot.get("nutrient_level", 85.0)

        issues = []
        recommendations = []
        priority = "LOW"
        affected_params = []
        confidence = 96.0

        if ph > 6.8:
            issues.append(f"Alkaline pH drift detected ({ph} pH). Iron and Manganese absorption blocked.")
            recommendations.append("Dose pH-Down solution to calibrate reservoir pH to 6.0.")
            priority = "HIGH"
            affected_params.append("water_ph")
        elif ph < 5.2:
            issues.append(f"Acidic pH drop detected ({ph} pH). Calcium and Magnesium lockout.")
            recommendations.append("Dose pH-Up solution to raise water pH to 6.0.")
            priority = "CRITICAL" if ph < 4.8 else "HIGH"
            affected_params.append("water_ph")

        if ec > 2.6:
            issues.append(f"High Electrical Conductivity ({ec} mS/cm). Salt buildup risk.")
            recommendations.append("Dilute reservoir solution with fresh RO water to lower EC.")
            if priority != "CRITICAL":
                priority = "HIGH"
            affected_params.append("water_ec")
        elif ec < 1.3:
            issues.append(f"Nutrient solution depletion ({ec} mS/cm). Crop starvation risk.")
            recommendations.append("Replenish A/B concentrated nutrient solution to target 2.0 mS/cm.")
            if priority not in ["CRITICAL", "HIGH"]:
                priority = "HIGH"
            affected_params.append("water_ec")

        if nutrient_level < 30.0:
            issues.append(f"Low nutrient tank volume level ({nutrient_level}%).")
            recommendations.append("Refill primary nutrient dosing reservoir tank.")
            if priority not in ["CRITICAL", "HIGH"]:
                priority = "MEDIUM"
            affected_params.append("nutrient_level")

        if not issues:
            analysis = "Hydroponic solution chemistry (pH 6.2, EC 2.0 mS/cm) is in optimal balance."
            rec_action = "Maintain current daily dosing rate."
        else:
            analysis = " ".join(issues)
            rec_action = " ".join(recommendations)

        return {
            "agent_name": "NutritionAgent",
            "decision_type": "Nutrition",
            "priority": priority,
            "title": "Hydroponic Solution Chemistry & Dosing Analysis",
            "analysis": analysis,
            "recommended_action": rec_action,
            "confidence_score": confidence,
            "affected_parameters": affected_params
        }
