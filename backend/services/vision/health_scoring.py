from backend.services.vision.disease_detector import VisionModel

class HealthScoring(VisionModel):
    """
    Calculates unified crop health score based on disease penalties,
    severity escalators, and biometric scores.
    """
    def predict(self, image_path: str) -> dict:
        return {"health_score": 100.0}

    @staticmethod
    def calculate_health_score(disease_results: dict, growth_results: dict) -> float:
        score = 100.0
        disease = disease_results.get("disease", "Healthy")
        severity = disease_results.get("severity", "None")

        if disease != "Healthy":
            penalties = {
                "Tip Burn": 15.0,
                "Nutrient Deficiency": 20.0,
                "Root Rot Symptoms": 55.0,
                "Leaf Spot": 25.0,
                "Yellow Leaves": 18.0,
                "Fungal Stress": 30.0
            }
            
            penalty = penalties.get(disease, 15.0)
            severity_mult = {
                "Low": 0.7,
                "Medium": 1.0,
                "High": 1.5,
                "None": 1.0
            }
            mult = severity_mult.get(severity, 1.0)
            score -= (penalty * mult)

        g_score = growth_results.get("growth_score", 90.0)
        score = (score * 0.95) + (g_score * 0.05)

        return round(max(0.0, min(100.0, score)), 2)
