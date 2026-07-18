from backend.services.digital_twin.growth_simulator import GrowthSimulator

class ScenarioEngine:
    """
    Evaluates modified farm variables relative to original baselines,
    projecting yield differentials and health offsets.
    """
    @staticmethod
    def run_scenario_comparison(original_conditions: dict, modified_conditions: dict, duration_days: int = 35) -> dict:
        orig_state = GrowthSimulator.calculate_daily_state(duration_days, original_conditions)
        mod_state = GrowthSimulator.calculate_daily_state(duration_days, modified_conditions)

        orig_yield = orig_state["predicted_weight"]
        mod_yield = mod_state["predicted_weight"]

        orig_health = orig_state["health_score"]
        mod_health = mod_state["health_score"]

        yield_change = 0.0
        if orig_yield > 0.0:
            yield_change = round(((mod_yield - orig_yield) / orig_yield) * 100.0, 2)

        health_change = round(mod_health - orig_health, 2)

        recs = []
        if mod_yield > orig_yield:
            recs.append("The proposed modifications show a positive yield improvement.")
        else:
            recs.append("The proposed modifications reduce yield. Revert to baseline settings.")

        if modified_conditions.get("temperature", 22.0) > 26.0:
            recs.append("High air temperature will increase leaf transpiration stress. Reduce cooling threshold.")
        if modified_conditions.get("water_ec", 2.0) > 2.5:
            recs.append("Elevated EC levels risk salt accumulation. Consider reducing nutrient dosing.")

        return {
            "original_yield": f"{orig_yield}g",
            "modified_yield": f"{mod_yield}g",
            "yield_difference": f"{'+' if yield_change >= 0 else ''}{yield_change}%",
            "yield_change_percentage": yield_change,
            "original_health": orig_health,
            "modified_health": mod_health,
            "health_difference": f"{'+' if health_change >= 0 else ''}{health_change}%",
            "recommendations": recs,
            "final_stage": mod_state["growth_stage"]
        }
