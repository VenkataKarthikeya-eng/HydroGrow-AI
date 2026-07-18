class GrowthSimulator:
    """
    Simulates daily biological crop growth metrics (height, weight, health)
    under varying environmental stress constraints.
    """
    @staticmethod
    def get_stage_for_day(day: int) -> str:
        if day <= 10:
            return "Seedling"
        elif day <= 25:
            return "Vegetative"
        elif day <= 35:
            return "Maturity"
        else:
            return "Harvest"

    @staticmethod
    def calculate_daily_state(day: int, conditions: dict) -> dict:
        stage = GrowthSimulator.get_stage_for_day(day)
        
        base_height = 2.0
        base_weight = 4.0
        
        temp = conditions.get("temperature", 22.0)
        humidity = conditions.get("humidity", 60.0)
        co2 = conditions.get("co2", 450.0)
        ec = conditions.get("water_ec", 2.0)
        ph = conditions.get("water_ph", 6.0)
        light_hours = conditions.get("light_hours", 16.0)

        # Penalties & modifiers relative to ideal letuuce inputs
        temp_factor = max(0.4, 1.0 - abs(temp - 22.0) * 0.04)
        humidity_factor = max(0.5, 1.0 - abs(humidity - 60.0) * 0.015)
        co2_factor = min(1.3, max(0.7, 1.0 + (co2 - 450.0) * 0.0005))
        ec_factor = max(0.3, 1.0 - abs(ec - 2.0) * 0.15)
        ph_factor = max(0.5, 1.0 - abs(ph - 6.0) * 0.2)
        light_factor = min(1.2, max(0.8, 1.0 + (light_hours - 16.0) * 0.03))

        total_mod = temp_factor * humidity_factor * co2_factor * ec_factor * ph_factor * light_factor

        if day <= 10:
            height = base_height + (day * 0.8 * total_mod)
            weight = base_weight + (day * 1.5 * total_mod)
        elif day <= 25:
            height = 10.0 + ((day - 10) * 1.2 * total_mod)
            weight = 19.0 + ((day - 10) * 12.0 * total_mod)
        elif day <= 35:
            height = 28.0 + ((day - 25) * 0.6 * total_mod)
            weight = 199.0 + ((day - 25) * 20.0 * total_mod)
        else:
            height = 34.0 + ((day - 35) * 0.1 * total_mod)
            weight = 399.0 + ((day - 35) * 10.0 * total_mod)

        health = 100.0 - (abs(temp - 22.0) * 1.5) - (abs(ec - 2.0) * 8.0) - (abs(ph - 6.0) * 12.0)
        health = round(max(0.0, min(100.0, health)), 2)

        return {
            "day": day,
            "predicted_height": round(height, 2),
            "predicted_weight": round(weight, 2),
            "health_score": health,
            "growth_stage": stage
        }
