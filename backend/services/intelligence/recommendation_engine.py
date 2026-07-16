"""
recommendation_engine.py — HydroGrow AI Upgraded Cultivation Recommendation Engine

This module provides rule-based agricultural recommendations for hydroponic
lettuce cultivation. Rules evaluate water, environmental, and seedling parameters
against agronomic thresholds for Lactuca sativa (lettuce), returning detailed explanations
and practical grow-room actions.
"""

# ---------------------------------------------------------------------------
# Upgraded Recommendation Generator
# ---------------------------------------------------------------------------
def generate_recommendations(user_inputs: dict) -> list:
    """
    Evaluate user inputs against hydroponic lettuce growing standards
    and return detailed agricultural recommendations.

    Parameters
    ----------
    user_inputs : dict
        The 13 user-facing input values from the dashboard.

    Returns
    -------
    list of dicts, each with:
        type      : "success" | "warning" | "critical"
        parameter : str (e.g., "Water pH")
        value     : str (formatted current value with unit)
        status    : "Optimal" | "Warning" | "Critical"
        message   : str (expert physiological explanation)
        action    : str (actionable growers advice)
    """
    recommendations = []

    # =======================================================================
    # 1. Water pH (Optimal: 5.5 - 6.5)
    # =======================================================================
    ph = float(user_inputs.get("water_ph", 6.2))
    ph_val = f"{ph:.1f}"
    
    if 5.5 <= ph <= 6.5:
        recommendations.append({
            "type": "success",
            "parameter": "Water pH",
            "value": ph_val,
            "status": "Optimal",
            "message": "Water pH is within the ideal lettuce growth range (5.5-6.5). This supports optimal nutrient solubility and prevents nutrient lockout.",
            "action": "Maintain current pH level and continue daily monitoring."
        })
    elif 5.0 <= ph < 5.5:
        recommendations.append({
            "type": "warning",
            "parameter": "Water pH",
            "value": ph_val,
            "status": "Warning",
            "message": "Water pH is slightly acidic (5.0-5.4). This level reduces the uptake of essential secondary macronutrients, particularly calcium and magnesium.",
            "action": "Gradually apply pH-up solution to return the system to the optimal 5.5-6.5 range."
        })
    elif 6.5 < ph <= 7.5:
        recommendations.append({
            "type": "warning",
            "parameter": "Water pH",
            "value": ph_val,
            "status": "Warning",
            "message": "Water pH is slightly alkaline (6.6-7.5). Iron, manganese, and phosphorus solubility drops significantly, which can cause leaf yellowing (chlorosis).",
            "action": "Gradually add pH-down solution to bring pH back into the optimal 5.5-6.5 range."
        })
    elif ph < 5.0:
        recommendations.append({
            "type": "critical",
            "parameter": "Water pH",
            "value": ph_val,
            "status": "Critical",
            "message": "Water pH is critically low (< 5.0). Extreme acidity damages root tissues (root burn) and completely locks out major nutrients like nitrogen, phosphorus, and potassium.",
            "action": "Immediately add pH-up solution. Check the dosing pumps for malfunction and flush the reservoir if stability cannot be restored."
        })
    else:  # ph > 7.5
        recommendations.append({
            "type": "critical",
            "parameter": "Water pH",
            "value": ph_val,
            "status": "Critical",
            "message": "Water pH is critically high (> 7.5). Severe nutrient lockout of phosphorus and micronutrients (especially iron) will arrest growth and cause severe chlorosis.",
            "action": "Add pH-down solution immediately. Calibrate the pH probe to ensure readings are accurate, and verify acid dosing systems."
        })

    # =======================================================================
    # 2. Water EC (Optimal: 1.2 - 2.5 mS/cm)
    # =======================================================================
    ec = float(user_inputs.get("water_ec", 2.0))
    ec_val = f"{ec:.2f} mS/cm"
    
    if 1.2 <= ec <= 2.5:
        recommendations.append({
            "type": "success",
            "parameter": "Water EC",
            "value": ec_val,
            "status": "Optimal",
            "message": "Electrical Conductivity (EC) is in the optimal range (1.2-2.5 mS/cm). This supplies sufficient salt concentrations for rapid vegetative growth without osmotic stress.",
            "action": "Keep current nutrient dosing rates and check EC levels daily."
        })
    elif 0.8 <= ec < 1.2:
        recommendations.append({
            "type": "warning",
            "parameter": "Water EC",
            "value": ec_val,
            "status": "Warning",
            "message": "Water EC is low (0.8-1.1 mS/cm). Underfeeding will result in slower leaf development and lighter-colored foliage due to sub-optimal nitrogen levels.",
            "action": "Slightly increase the nutrient dosing rate to raise EC towards 1.5 mS/cm."
        })
    elif 2.5 < ec <= 3.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Water EC",
            "value": ec_val,
            "status": "Warning",
            "message": "Water EC is elevated (2.6-3.0 mS/cm). High salinity increases osmotic pressure, making it harder for the roots to draw water, which can trigger tip burn.",
            "action": "Dilute the reservoir with fresh, pH-adjusted water to bring the EC back under 2.5 mS/cm."
        })
    elif ec < 0.8:
        recommendations.append({
            "type": "critical",
            "parameter": "Water EC",
            "value": ec_val,
            "status": "Critical",
            "message": "Water EC is critically low (< 0.8 mS/cm). Severe nutrient starvation will stunt growth, causing leaves to yellow and root systems to exhaust reserves.",
            "action": "Immediately add balanced A/B nutrient stock solutions to raise the EC to at least 1.2 mS/cm."
        })
    else:  # ec > 3.0
        recommendations.append({
            "type": "critical",
            "parameter": "Water EC",
            "value": ec_val,
            "status": "Critical",
            "message": "Water EC is critically high (> 3.0 mS/cm). Extreme osmotic stress can dry out leaf tips (reverse osmosis) and permanently damage root cells.",
            "action": "Immediately drain a portion of the nutrient solution and top off the reservoir with pure water to dilute the EC below 2.5 mS/cm."
        })

    # =======================================================================
    # 3. Air Temperature (Optimal: 18 - 24 °C)
    # =======================================================================
    air_temp = float(user_inputs.get("air_temperature", 22.0))
    air_temp_val = f"{air_temp:.1f} °C"
    
    if 18.0 <= air_temp <= 24.0:
        recommendations.append({
            "type": "success",
            "parameter": "Air Temperature",
            "value": air_temp_val,
            "status": "Optimal",
            "message": "Air temperature is in the optimal range (18-24°C). This maximizes the rate of photosynthesis while keeping transpiration rates balanced.",
            "action": "Maintain current HVAC setpoints and ventilation schedules."
        })
    elif 15.0 <= air_temp < 18.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Air Temperature",
            "value": air_temp_val,
            "status": "Warning",
            "message": "Air temperature is cool (15.0-17.9°C). Root metabolic activity and cellular growth slow down, extending the total crop cycle.",
            "action": "Increase heater setpoints or reduce exhaust fan speed slightly if humidity allows."
        })
    elif 24.0 < air_temp <= 28.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Air Temperature",
            "value": air_temp_val,
            "status": "Warning",
            "message": "Air temperature is warm (24.1-28.0°C). Warm air increases transpiration, raising the risk of calcium-related tip burn and early bolting.",
            "action": "Increase airflow using fans, activate cooling pads, or draw shade screens during peak sunlight."
        })
    elif air_temp < 15.0:
        recommendations.append({
            "type": "critical",
            "parameter": "Air Temperature",
            "value": air_temp_val,
            "status": "Critical",
            "message": "Air temperature is critically cold (< 15.0°C). Severe cold stunts growth, limits nutrient mobility inside the plant, and can cause cold injury.",
            "action": "Immediately activate heaters. Check greenhouse insulation and verify HVAC heating circuits are operating."
        })
    else:  # air_temp > 28.0
        recommendations.append({
            "type": "critical",
            "parameter": "Air Temperature",
            "value": air_temp_val,
            "status": "Critical",
            "message": "Air temperature is critically high (> 28.0°C). Heat stress triggers immediate bolting (premature flowering), bitter leaf flavors, and tip burn.",
            "action": "Turn on all exhaust fans, activate active evaporative cooling/air conditioning, and maximize shade cover."
        })

    # =======================================================================
    # 4. Humidity (Optimal: 50 - 70 %)
    # =======================================================================
    humidity = float(user_inputs.get("humidity", 60.0))
    humidity_val = f"{humidity:.1f} %"
    
    if 50.0 <= humidity <= 70.0:
        recommendations.append({
            "type": "success",
            "parameter": "Humidity",
            "value": humidity_val,
            "status": "Optimal",
            "message": "Relative humidity is in the optimal range (50-70%). This supports a steady transpiration rate, ensuring calcium reaches the growing leaf tips to prevent tip burn.",
            "action": "Maintain current ventilation and air circulation settings."
        })
    elif 40.0 <= humidity < 50.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Humidity",
            "value": humidity_val,
            "status": "Warning",
            "message": "Humidity is low (40.0-49.9%). Dry air accelerates transpiration, which can cause stress and moisture loss in young lettuce seedlings.",
            "action": "Increase humidity levels using misting lines or by lowering exhaust fan speeds."
        })
    elif 70.0 < humidity <= 80.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Humidity",
            "value": humidity_val,
            "status": "Warning",
            "message": "Humidity is high (70.1-80.0%). Reduced transpiration slows down calcium transport, which paradoxically increases the risk of tip burn.",
            "action": "Increase internal air circulation using oscillating fans and run dehumidifiers."
        })
    elif humidity < 40.0:
        recommendations.append({
            "type": "critical",
            "parameter": "Humidity",
            "value": humidity_val,
            "status": "Critical",
            "message": "Humidity is critically dry (< 40.0%). Plants will close their stomata to prevent dehydration, halting photosynthesis and stunting growth.",
            "action": "Turn on humidifiers or misting systems immediately. Keep the root zone saturated to prevent wilting."
        })
    else:  # humidity > 80.0
        recommendations.append({
            "type": "critical",
            "parameter": "Humidity",
            "value": humidity_val,
            "status": "Critical",
            "message": "Humidity is critically high (> 80.0%). Stagnant moisture promotes fungal diseases like Botrytis (grey mould) and downy mildew, which can ruin the crop.",
            "action": "Activate exhaust fans, run commercial dehumidifiers, and turn on circulating fans to prevent water condensation on leaves."
        })

    # =======================================================================
    # 5. CO2 Level (Productive: 400 - 800 ppm)
    # =======================================================================
    co2 = float(user_inputs.get("co2", 450.0))
    co2_val = f"{co2:.0f} ppm"
    
    if 400.0 <= co2 <= 800.0:
        recommendations.append({
            "type": "success",
            "parameter": "CO2 Level",
            "value": co2_val,
            "status": "Optimal",
            "message": "CO2 level is in the productive range (400-800 ppm). This concentration optimizes carbon fixation, accelerating photosynthetic activity.",
            "action": "Continue current CO2 injection rates during light cycles."
        })
    elif 300.0 <= co2 < 400.0:
        recommendations.append({
            "type": "warning",
            "parameter": "CO2 Level",
            "value": co2_val,
            "status": "Warning",
            "message": "CO2 is low (300.0-399.9 ppm), bordering ambient depletion. Photosynthesis is limited by carbon availability, reducing growth speed.",
            "action": "Increase ventilation to draw in fresh ambient air, or supplement with CO2 during light periods."
        })
    elif 800.0 < co2 <= 1000.0:
        recommendations.append({
            "type": "warning",
            "parameter": "CO2 Level",
            "value": co2_val,
            "status": "Warning",
            "message": "CO2 level is high (800.1-1000.0 ppm). While lettuce tolerate this, returns diminish above 800 ppm and can become uneconomical.",
            "action": "Check the CO2 regulator flow rate and monitor sensor calibrations."
        })
    elif co2 < 300.0:
        recommendations.append({
            "type": "critical",
            "parameter": "CO2 Level",
            "value": co2_val,
            "status": "Critical",
            "message": "CO2 level is critically depleted (< 300.0 ppm). Severe carbon starvation halts photosynthetic output and halts lettuce development.",
            "action": "Vigorously ventilate the grow area immediately or verify that the CO2 dosing system is active."
        })
    else:  # co2 > 1000.0
        recommendations.append({
            "type": "critical",
            "parameter": "CO2 Level",
            "value": co2_val,
            "status": "Critical",
            "message": "CO2 level is critically high (> 1000.0 ppm). Excess CO2 can induce stomatal closure, damage leaves, and presents a hazard to greenhouse workers.",
            "action": "Shut off CO2 injection immediately, exhaust the air from the grow space, and check the sensor calibration."
        })

    # =======================================================================
    # 6. Water Temperature (Optimal: 18 - 24 °C)
    # =======================================================================
    water_temp = float(user_inputs.get("water_temperature", 23.0))
    water_temp_val = f"{water_temp:.1f} °C"
    
    if 18.0 <= water_temp <= 24.0:
        recommendations.append({
            "type": "success",
            "parameter": "Water Temperature",
            "value": water_temp_val,
            "status": "Optimal",
            "message": "Water temperature is in the optimal range (18-24°C). This maintains a healthy balance of dissolved oxygen and root cell respiration.",
            "action": "Monitor reservoir temperature to maintain stability."
        })
    elif 15.0 <= water_temp < 18.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Water Temperature",
            "value": water_temp_val,
            "status": "Warning",
            "message": "Water temperature is cool (15.0-17.9°C). Cool water slows root respiration and slows down nutrient uptake rates.",
            "action": "Consider installing a small reservoir heater, or insulate lines exposed to cold drafts."
        })
    elif 24.0 < water_temp <= 26.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Water Temperature",
            "value": water_temp_val,
            "status": "Warning",
            "message": "Water temperature is warm (24.1-26.0°C). Dissolved oxygen levels in the water drop, stressing roots and promoting pathogen activity.",
            "action": "Insulate the reservoir, draw reservoir shades, or run a water chiller."
        })
    elif water_temp < 15.0:
        recommendations.append({
            "type": "critical",
            "parameter": "Water Temperature",
            "value": water_temp_val,
            "status": "Critical",
            "message": "Water temperature is critically cold (< 15.0°C). Severe cold shock damages root tips and restricts water/nutrient transport, stunting growth.",
            "action": "Turn on a reservoir heater immediately to raise the water temperature above 18°C."
        })
    else:  # water_temp > 26.0
        recommendations.append({
            "type": "critical",
            "parameter": "Water Temperature",
            "value": water_temp_val,
            "status": "Critical",
            "message": "Water temperature is critically hot (> 26.0°C). Deoxygenated water suffocates roots, leading to root rot (Pythium) and rapid crop failure.",
            "action": "Use a water chiller or ice packs to drop temperatures immediately. Add aeration (air stones) and hydrogen peroxide to sanitize roots."
        })

    # =======================================================================
    # 7. Nutrient Solution Added (Optimal: 200 - 600 mL)
    # =======================================================================
    nutrient_ml = float(user_inputs.get("nutrient_solution_ml", 400.0))
    nutrient_val = f"{nutrient_ml:.0f} mL"
    
    if 200.0 <= nutrient_ml <= 600.0:
        recommendations.append({
            "type": "success",
            "parameter": "Nutrient Solution Added",
            "value": nutrient_val,
            "status": "Optimal",
            "message": "Total nutrient solution added is appropriate for this scale, maintaining stable background salt reserves.",
            "action": "Maintain current replenishment schedule."
        })
    elif 100.0 <= nutrient_ml < 200.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Nutrient Solution Added",
            "value": nutrient_val,
            "status": "Warning",
            "message": "Nutrient solution volume added is low. Over time, the plant will deplete the reservoir nutrients, leading to deficiencies.",
            "action": "Top up the reservoir and check the automated dosing pump settings."
        })
    elif nutrient_ml > 600.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Nutrient Solution Added",
            "value": nutrient_val,
            "status": "Warning",
            "message": "Nutrient solution volume added is high. Excess dosage risks running high EC levels and salt toxicities if not diluted.",
            "action": "Monitor EC levels closely and ensure fresh water refills are balanced."
        })
    else:  # nutrient_ml < 100.0
        recommendations.append({
            "type": "critical",
            "parameter": "Nutrient Solution Added",
            "value": nutrient_val,
            "status": "Critical",
            "message": "Nutrient solution volume added is critically low. Severe starvation is imminent once background ions are depleted.",
            "action": "Manually add nutrient concentrate immediately and verify dosing pump functionality."
        })

    # =======================================================================
    # 8. Water Consumption (Optimal: 50 - 300 L)
    # =======================================================================
    water_l = float(user_inputs.get("water_consumption_l", 170.0))
    water_val = f"{water_l:.1f} L"
    
    if 50.0 <= water_l <= 300.0:
        recommendations.append({
            "type": "success",
            "parameter": "Water Consumption",
            "value": water_val,
            "status": "Optimal",
            "message": "System water consumption is within normal limits, reflecting healthy plant transpiration rates.",
            "action": "Maintain standard reservoir top-up schedules."
        })
    elif water_l < 50.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Water Consumption",
            "value": water_val,
            "status": "Warning",
            "message": "Water consumption is low. This suggests low transpiration rates, potentially due to high humidity, cold, or root sickness.",
            "action": "Check humidity levels, look for signs of root rot, and verify that the pump flow rate is adequate."
        })
    else:  # water_l > 300.0
        recommendations.append({
            "type": "warning",
            "parameter": "Water Consumption",
            "value": water_val,
            "status": "Warning",
            "message": "Water consumption is exceptionally high. This could indicate normal high transpiration from massive plants, or a physical leak.",
            "action": "Inspect grow channels, reservoir tanks, and plumbing fittings for leaks."
        })

    # =======================================================================
    # 9. Seedling Condition (Weight, Height, Root Length)
    # =======================================================================
    init_weight = float(user_inputs.get("initial_weight_g", 4.0))
    init_weight_val = f"{init_weight:.2f} g"
    if 2.0 <= init_weight <= 5.0:
        recommendations.append({
            "type": "success",
            "parameter": "Seedling Starting Weight",
            "value": init_weight_val,
            "status": "Optimal",
            "message": "Starting seedling weight is ideal, indicating robust vegetative tissue and carbohydrate reserves.",
            "action": "Proceed with standard transplanting protocol."
        })
    elif init_weight < 2.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Seedling Starting Weight",
            "value": init_weight_val,
            "status": "Warning",
            "message": "Starting seedling weight is low. Underdeveloped seedlings have higher transplant mortality and take longer to establish.",
            "action": "Provide a mild nutrient solution (EC 1.0) and high humidity to support early establishment."
        })
    else:  # init_weight > 5.0
        recommendations.append({
            "type": "warning",
            "parameter": "Seedling Starting Weight",
            "value": init_weight_val,
            "status": "Warning",
            "message": "Starting seedling weight is high. Overmature seedlings can suffer from root binding and transplant shock.",
            "action": "Handle roots carefully during transplanting to minimize transplant shock."
        })

    init_height = float(user_inputs.get("initial_height_cm", 12.0))
    init_height_val = f"{init_height:.1f} cm"
    if 10.0 <= init_height <= 15.0:
        recommendations.append({
            "type": "success",
            "parameter": "Seedling Starting Height",
            "value": init_height_val,
            "status": "Optimal",
            "message": "Starting seedling height is optimal, showing good canopy growth without stretching.",
            "action": "Transplant into standard growing channels."
        })
    elif init_height < 10.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Seedling Starting Height",
            "value": init_height_val,
            "status": "Warning",
            "message": "Starting seedling height is short. Small seedlings may struggle to compete for light if spaced too closely.",
            "action": "Ensure even lighting distribution and avoid placing next to larger seedlings."
        })
    else:  # init_height > 15.0
        recommendations.append({
            "type": "warning",
            "parameter": "Seedling Starting Height",
            "value": init_height_val,
            "status": "Warning",
            "message": "Starting seedling height is tall. This indicates etiolation (stretching) due to insufficient light in the nursery.",
            "action": "Increase light intensity in the nursery phase for future batches."
        })

    init_root = float(user_inputs.get("initial_root_length_cm", 7.0))
    init_root_val = f"{init_root:.1f} cm"
    if 5.0 <= init_root <= 10.0:
        recommendations.append({
            "type": "success",
            "parameter": "Seedling Starting Root Length",
            "value": init_root_val,
            "status": "Optimal",
            "message": "Seedling root length is in the optimal range, showing healthy root branching.",
            "action": "Ensure roots are properly suspended in the flow channels."
        })
    elif init_root < 5.0:
        recommendations.append({
            "type": "warning",
            "parameter": "Seedling Starting Root Length",
            "value": init_root_val,
            "status": "Warning",
            "message": "Seedling root length is short. Underdeveloped roots will struggle to reach the nutrient stream in the grow channels.",
            "action": "Slightly increase water level in the grow channels until roots grow longer."
        })
    else:  # init_root > 10.0
        recommendations.append({
            "type": "warning",
            "parameter": "Seedling Starting Root Length",
            "value": init_root_val,
            "status": "Warning",
            "message": "Seedling roots are exceptionally long, which can cause tangling or lead to channel clogs.",
            "action": "Trim roots slightly if necessary, or carefully direct them along the channel bottom to prevent drainage blockages."
        })

    return recommendations


# ---------------------------------------------------------------------------
# Standalone test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Test with a scenario that triggers various recommendations
    test_inputs = {
        "water_ph": 4.5,            # critical low
        "water_ec": 3.2,            # critical high
        "water_tds": 1.5,
        "water_temperature": 27.0,  # critical high
        "air_temperature": 25.5,    # warning high
        "humidity": 45.0,           # warning low
        "co2": 280.0,               # critical low
        "nutrient_solution_ml": 80.0,     # critical low
        "water_consumption_l": 40.0,      # warning low
        "acid_consumption_ml": 10.0,
        "initial_height_cm": 8.0,         # warning low
        "initial_weight_g": 6.0,          # warning high
        "initial_root_length_cm": 12.0,   # warning high
    }

    import json
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    print("=" * 70)
    print("HydroGrow AI — Upgraded Recommendation Engine Test")
    print("=" * 70)

    recs = generate_recommendations(test_inputs)
    for i, rec in enumerate(recs, 1):
        icon = {"warning": "⚠️", "critical": "🚨", "success": "✅"}.get(rec["type"], "•")
        print(f"\n{i}. [{icon} {rec['type'].upper()} — {rec['status']}] {rec['parameter']} ({rec['value']})")
        print(f"   Explanation: {rec['message']}")
        print(f"   Action:      {rec['action']}")

    print(f"\n--- Total recommendations: {len(recs)} ---")
    print("Recommendation engine upgrade test completed successfully!")
