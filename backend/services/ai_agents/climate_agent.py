class ClimateAgent:
    """
    Autonomous sub-agent evaluating environmental sensor conditions
    and atmospheric stability.
    """

    @staticmethod
    def run(context: dict) -> dict:
        iot = context.get("iot_info", {})
        temp = iot.get("temperature", 22.0)
        humidity = iot.get("humidity", 60.0)
        co2 = iot.get("co2", 450.0)
        water_temp = iot.get("water_temperature", 21.0)

        issues = []
        recommendations = []
        priority = "LOW"
        affected_params = []
        confidence = 94.0

        if temp > 28.0:
            issues.append(f"Heat stress detected (Air Temp {temp}°C).")
            recommendations.append("Activate cooling fan relays and deploy shade screens immediately.")
            priority = "CRITICAL" if temp > 31.0 else "HIGH"
            affected_params.append("temperature")
        elif temp < 16.0:
            issues.append(f"Low ambient temperature detected ({temp}°C).")
            recommendations.append("Engage greenhouse heating units to elevate air temperature to 22°C.")
            priority = "HIGH"
            affected_params.append("temperature")

        if humidity > 80.0:
            issues.append(f"High air humidity detected ({humidity}%). Risk of fungal mold growth.")
            recommendations.append("Activate dehumidification and ventilation exhaust systems.")
            if priority != "CRITICAL":
                priority = "HIGH"
            affected_params.append("humidity")

        if co2 < 350.0:
            issues.append(f"CO2 deficit detected ({co2} ppm). Photosynthesis rate reduced.")
            recommendations.append("Open fresh air intake vents or activate CO2 injection system.")
            if priority not in ["CRITICAL", "HIGH"]:
                priority = "MEDIUM"
            affected_params.append("co2")

        if water_temp > 25.0:
            issues.append(f"High water temperature detected ({water_temp}°C). Pythium root rot threat.")
            recommendations.append("Activate reservoir water chiller or inject oxygenation aeration.")
            priority = "CRITICAL"
            affected_params.append("water_temperature")

        if not issues:
            analysis = "Environmental climate parameters (air temp, humidity, CO2, water temp) are optimal."
            rec_action = "Maintain current climate control setpoints."
        else:
            analysis = " ".join(issues)
            rec_action = " ".join(recommendations)

        return {
            "agent_name": "ClimateAgent",
            "decision_type": "Climate",
            "priority": priority,
            "title": "Greenhouse Climate & Environmental Stress Analysis",
            "analysis": analysis,
            "recommended_action": rec_action,
            "confidence_score": confidence,
            "affected_parameters": affected_params
        }
