class OptimizationStrategy:
    """
    Formulates agronomic optimizations to correct warnings and boost crop yield.
    """
    @staticmethod
    def formulate_strategies(conditions: dict) -> list:
        strategies = []
        
        temp = conditions.get("temperature", 22.0)
        ec = conditions.get("water_ec", 2.0)
        ph = conditions.get("water_ph", 6.0)
        humidity = conditions.get("humidity", 60.0)

        if temp > 25.0:
            strategies.append({
                "parameter": "Temperature",
                "current": f"{temp}°C",
                "recommendation": "Reduce temperature to 23°C",
                "impact": "+12% biomass increase"
            })
        elif temp < 18.0:
            strategies.append({
                "parameter": "Temperature",
                "current": f"{temp}°C",
                "recommendation": "Increase heating to 22°C",
                "impact": "+8% biomass increase"
            })

        if ec > 2.4:
            strategies.append({
                "parameter": "Water EC",
                "current": f"{ec} mS/cm",
                "recommendation": "Reduce nutrient dosing to 2.0 EC",
                "impact": "+15% quality increase (prevents tip burn)"
            })
        elif ec < 1.4:
            strategies.append({
                "parameter": "Water EC",
                "current": f"{ec} mS/cm",
                "recommendation": "Increase nutrient dosing to 1.8 EC",
                "impact": "+20% weight increase"
            })

        if ph > 6.5:
            strategies.append({
                "parameter": "Water pH",
                "current": ph,
                "recommendation": "Dose pH-Down to target 6.0",
                "impact": "+10% macro absorption rate"
            })
        elif ph < 5.5:
            strategies.append({
                "parameter": "Water pH",
                "current": ph,
                "recommendation": "Dose pH-Up to target 6.0",
                "impact": "+15% root health protection"
            })

        if not strategies:
            strategies.append({
                "parameter": "Environment",
                "current": "Optimal",
                "recommendation": "Maintain current setpoints",
                "impact": "Stable harvest"
            })

        return strategies
