class HealthModel:
    """
    Plant Health Score Synthesizer (0-100).
    Combines Vision Pathology, IoT Telemetry, and Growth Metrics.
    """

    @staticmethod
    def calculate_health_score(vision_res: dict, iot_res: dict, growth_res: dict) -> float:
        base_score = vision_res.get("health_score", 95.0)

        # Environmental deductions
        temp = iot_res.get("temperature", 22.0)
        ph = iot_res.get("water_ph", 6.2)
        ec = iot_res.get("water_ec", 2.0)

        if temp > 28.0 or temp < 16.0:
            base_score -= 10.0
        if ph < 5.2 or ph > 6.8:
            base_score -= 15.0
        if ec < 1.3 or ec > 2.5:
            base_score -= 10.0

        # Growth performance adjustment
        fresh_weight = growth_res.get("fresh_weight", 250.0)
        if fresh_weight >= 300.0:
            base_score += 5.0

        return round(max(0.0, min(100.0, base_score)), 1)
