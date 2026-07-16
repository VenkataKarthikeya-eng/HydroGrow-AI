"""
explanation_engine.py — HydroGrow AI Prediction Explanation Module

This module analyzes user inputs, validated predictions, and recommendation outputs
to provide expert-level, explainable AI diagnostics for hydroponic lettuce cultivation.
"""

def generate_explanation(user_inputs: dict, validated_prediction_result: dict, recommendation_outputs: list) -> dict:
    """
    Generate an explainable AI diagnostics structure based on inference results and crop recommendations.

    Parameters
    ----------
    user_inputs : dict
        The 13 user-facing inputs.
    validated_prediction_result : dict
        The output dictionary from the prediction pipeline (with validation details).
    recommendation_outputs : list
        The list of dictionaries returned by the recommendation engine.

    Returns
    -------
    dict
        {
            "summary": str,
            "positive_factors": list,
            "improvement_opportunities": list,
            "confidence_explanation": str
        }
    """
    # 1. Prediction Summary
    weight = validated_prediction_result.get("prediction_value", 0.0)
    category = validated_prediction_result.get("growth_category", "Poor")
    
    # Strip any emojis from category if we want clean text, but keep it matching existing UI
    summary = (
        f"HydroGrow AI predicts {weight:.1f}g fresh weight. "
        f"The crop performance is classified as {category} based on training distribution."
    )

    # 2. Positive Growth Factors & Improvement Opportunities
    positive_factors = []
    improvement_opportunities = []

    # Map of custom explanations for optimal parameters
    optimal_explanations = {
        "Water pH": "Water pH ({value}) is optimal and supports nutrient absorption.",
        "Water EC": "EC ({value}) indicates balanced nutrient availability.",
        "Air Temperature": "Air temperature ({value}) supports active lettuce metabolism.",
        "Humidity": "Relative humidity ({value}) is optimal, supporting transpiration and calcium transport.",
        "CO2 Level": "CO2 level ({value}) is productive, supporting photosynthesis.",
        "Water Temperature": "Water temperature ({value}) is optimal, balancing dissolved oxygen and root respiration.",
        "Nutrient Solution Added": "Nutrient solution volume added ({value}) is appropriate for the scale of this hydroponic system.",
        "Water Consumption": "System water consumption ({value}) is within normal limits, reflecting healthy plant transpiration.",
        "Seedling Starting Weight": "Starting seedling weight ({value}) is ideal, indicating robust vegetative tissue and carbohydrate reserves.",
        "Seedling Starting Height": "Starting seedling height ({value}) is optimal, showing good canopy growth without stretching.",
        "Seedling Starting Root Length": "Seedling root length ({value}) is in the optimal range, showing healthy root branching."
    }

    # Extract current parameters
    ph = float(user_inputs.get("water_ph", 6.2))
    ec = float(user_inputs.get("water_ec", 2.0))
    air_temp = float(user_inputs.get("air_temperature", 22.0))
    humidity = float(user_inputs.get("humidity", 60.0))
    co2 = float(user_inputs.get("co2", 450.0))
    water_temp = float(user_inputs.get("water_temperature", 23.0))

    for rec in recommendation_outputs:
        param = rec["parameter"]
        val = rec["value"]
        
        if rec["type"] == "success":
            # Dynamic optimal explanation
            exp = optimal_explanations.get(
                param, 
                f"{param} ({val}) is in the optimal range, promoting healthy growth."
            )
            positive_factors.append({
                "factor": param,
                "impact": "positive",
                "explanation": exp.format(value=val)
            })
        else:
            # Dynamic out-of-range improvement opportunity
            exp = ""
            if param == "Water pH":
                if ph < 5.0:
                    exp = f"Water pH ({val}) is critically low, causing root damage (root burn) and complete lockout of major macronutrients."
                elif ph < 5.5:
                    exp = f"Water pH ({val}) is slightly low, reducing calcium and magnesium absorption. Adjusting pH upwards will prevent nutrient lockout."
                elif ph > 7.5:
                    exp = f"Water pH ({val}) is critically high, causing severe lockout of phosphorus and iron. Adjusting pH downwards will prevent leaf yellowing."
                else:
                    exp = f"Water pH ({val}) is slightly high, reducing solubility of iron, manganese, and phosphorus. Adjusting pH downwards will prevent chlorosis."
            elif param == "Water EC":
                if ec < 0.8:
                    exp = f"Water EC ({val}) is critically low, causing severe starvation, stunted growth, and pale foliage."
                elif ec < 1.2:
                    exp = f"Water EC ({val}) is low. Slightly increasing nutrient concentration will supply sufficient ions for vegetative growth."
                elif ec > 3.0:
                    exp = f"Water EC ({val}) is critically high, causing reverse osmosis and root damage. Diluting the solution will restore osmotic balance."
                else:
                    exp = f"Water EC ({val}) is high, causing osmotic stress and risk of leaf tip burn. Diluting the solution will restore optimal water uptake."
            elif param == "Air Temperature":
                if air_temp < 15.0:
                    exp = f"Air temperature ({val}) is critically low, stunting growth and stopping cell development. Warming is urgently needed."
                elif air_temp < 18.0:
                    exp = f"Air temperature ({val}) is cool, extending the total crop cycle. Warming the environment will accelerate growth."
                elif air_temp > 28.0:
                    exp = f"Air temperature ({val}) is critically high, causing immediate bolting (flowering) and bitter flavors."
                else:
                    exp = f"Air temperature ({val}) is warm, increasing transpiration and risks of bolting or tip burn. Cooling will prevent leaf damage."
            elif param == "Humidity":
                if humidity < 40.0:
                    exp = f"Relative humidity ({val}) is critically low, forcing stomata to close. Raising humidity will protect seedlings from drying out."
                elif humidity < 50.0:
                    exp = f"Relative humidity ({val}) is low, causing transpirational stress. Raising humidity will support young leaf margins."
                elif humidity > 80.0:
                    exp = f"Relative humidity ({val}) is critically high, promoting Botrytis (grey mould) and downy mildew. Dehumidifying is vital."
                else:
                    exp = f"Relative humidity ({val}) is high, restricting calcium uptake at leaf tips. Dehumidifying will support calcium transport."
            elif param == "CO2 Level":
                if co2 < 300.0:
                    exp = f"CO2 level ({val}) is critically depleted. Photosynthesis is severely limited; carbon enrichment is needed."
                elif co2 < 400.0:
                    exp = "CO2 level is below the ideal productivity range. Increasing CO2 availability may improve photosynthesis."
                elif co2 > 1000.0:
                    exp = f"CO2 level ({val}) is critically high, causing stomatal closure and hazards to operators. Venting the space is required."
                else:
                    exp = f"CO2 level ({val}) is high. While lettuce can tolerate it, reducing injection will prevent waste and ensure safety."
            elif param == "Water Temperature":
                if water_temp < 15.0:
                    exp = f"Water temperature ({val}) is critically cold, damaging root tips and restricting transport. Warming the reservoir is required."
                elif water_temp < 18.0:
                    exp = f"Water temperature ({val}) is cool, slowing root respiration. Warming the reservoir will improve nutrient absorption."
                elif water_temp > 26.0:
                    exp = f"Water temperature ({val}) is critically high, suffocating roots and inviting Pythium (root rot). Cooling is needed immediately."
                else:
                    exp = f"Water temperature ({val}) is warm, reducing dissolved oxygen and encouraging algae. Cooling is needed to protect root health."
            elif param == "Nutrient Solution Added":
                exp = f"Nutrient solution volume added ({val}) is sub-optimal. Adjusting nutrient dosing will prevent starvation or salt buildup."
            elif param == "Water Consumption":
                exp = f"System water consumption ({val}) is outside normal ranges, which may indicate transpiration issues or a leak in the system."
            elif param == "Seedling Starting Weight":
                exp = f"Starting seedling weight ({val}) is sub-optimal. Adjusting nursery lighting and EC can help seedlings establish."
            elif param == "Seedling Starting Height":
                exp = f"Starting seedling height ({val}) is sub-optimal. Ensure proper lighting in the nursery to prevent stretching."
            elif param == "Seedling Starting Root Length":
                exp = f"Seedling root length ({val}) is sub-optimal. Adjusting water levels in grow channels can support shorter roots or prevent clogs."
            else:
                exp = f"{param} ({val}) is outside the optimal range. Adjusting this parameter can enhance crop growth conditions."

            improvement_opportunities.append({
                "factor": param,
                "impact": "improvement",
                "explanation": exp
            })

    # 3. Model Confidence Explanation
    confidence_explanation = (
        "Prediction confidence is based on similarity between provided conditions "
        "and the 216 training samples."
    )

    return {
        "summary": summary,
        "positive_factors": positive_factors,
        "improvement_opportunities": improvement_opportunities,
        "confidence_explanation": confidence_explanation
    }
