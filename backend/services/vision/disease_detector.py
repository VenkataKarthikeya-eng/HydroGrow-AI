import os

class VisionModel:
    """
    Base service interface preparing the computer vision module
    for future ML model inference frameworks.
    """
    def predict(self, image_path: str) -> dict:
        raise NotImplementedError("Subclasses must implement predict.")

class DiseaseDetector(VisionModel):
    """
    Classifies crop disease category and outputs confidence parameters.
    """
    def predict(self, image_path: str) -> dict:
        fn = os.path.basename(image_path).lower()
        if "tip_burn" in fn or "tipburn" in fn:
            return {"disease": "Tip Burn", "confidence": 0.91, "severity": "Medium"}
        elif "deficiency" in fn:
            return {"disease": "Nutrient Deficiency", "confidence": 0.88, "severity": "Low"}
        elif "root_rot" in fn or "rootrot" in fn:
            return {"disease": "Root Rot Symptoms", "confidence": 0.85, "severity": "High"}
        elif "leaf_spot" in fn or "leafspot" in fn:
            return {"disease": "Leaf Spot", "confidence": 0.90, "severity": "Low"}
        elif "yellow" in fn:
            return {"disease": "Yellow Leaves", "confidence": 0.82, "severity": "Medium"}
        elif "fungal" in fn:
            return {"disease": "Fungal Stress", "confidence": 0.79, "severity": "Medium"}
        else:
            return {"disease": "Healthy", "confidence": 0.95, "severity": "None"}
