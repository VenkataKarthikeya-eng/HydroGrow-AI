class VisionRecommendation:
    """
    Generates tailored agronomic recovery recommendations based on
    detected plant disease types and stress severities.
    """
    @staticmethod
    def generate_recommendations(disease: str, severity: str) -> list:
        recs = []
        if disease == "Tip Burn":
            recs.append("Reduce reservoir EC level by 0.2 mS/cm.")
            recs.append("Increase calcium availability in the nutrient solution.")
            recs.append("Adjust relative humidity setpoint to target 65%.")
            recs.append("Ensure grow room circulation fans are operational to promote leaf transpiration.")
        elif disease == "Nutrient Deficiency":
            recs.append("Check solution EC level; supplement nutrient dosing rates by 10-15%.")
            recs.append("Calibrate pH sensors; maintain pH strictly between 5.8-6.2.")
            recs.append("Inspect roots for lockout signals.")
        elif disease == "Root Rot Symptoms":
            recs.append("Immediately flush and sanitize the hydroponic reservoir.")
            recs.append("Dose reservoir with hydrogen peroxide or beneficial microbes.")
            recs.append("Verify air stones are clean and oxygenating solution properly.")
            recs.append("Lower reservoir water temperature below 20°C.")
        elif disease == "Leaf Spot":
            recs.append("Prune infected leaves to restrict spores dispersion.")
            recs.append("Increase ventilation to drop humidity levels under 60%.")
            recs.append("Clean channel covers and sanitize surrounding assets.")
        elif disease == "Yellow Leaves":
            recs.append("Inspect for light height mapping (mitigate light burn or shade).")
            recs.append("Verify nitrogen concentration in your nutrient formula.")
        elif disease == "Fungal Stress":
            recs.append("Reduce relative humidity immediately to 55-60%.")
            recs.append("Apply organic crop-safe bio-fungicide treatments.")
        else:
            recs.append("Maintain current optimal environmental ranges.")
            recs.append("Continue daily validation of EC and pH calibration levels.")
            
        return recs
