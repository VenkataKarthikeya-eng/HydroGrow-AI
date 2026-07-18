import re

class IntentClassifier:
    """
    Classifies user agricultural queries into structured agronomic intents.
    """
    @staticmethod
    def classify_intent(message: str, resolved_query: str) -> str:
        clean_msg = message.lower().strip()
        clean_resolved = resolved_query.lower().strip()

        # 1. previous_prediction_analysis
        pred_analysis_words = [
            "previous", "past", "last prediction", "last run", "last week", 
            "yesterday", "earlier", "history", "former", "before", "history logs"
        ]
        if any(re.search(r'\b' + re.escape(w) + r'\b', clean_msg) for w in pred_analysis_words) and \
           any(re.search(r'\b(?:prediction|predicted|weight|g|crop|lettuce)\b', clean_msg) for w in ["prediction", "weight"]):
            return "previous_prediction_analysis"

        # 2. prediction_diagnostic (checking current predicted weight / why predicted weight is low)
        diag_words = ["why", "explain prediction", "only", "low", "predicted", "result", "weight", "prediction"]
        if any(re.search(r'\b' + re.escape(w) + r'\b', clean_resolved) for w in diag_words):
            return "prediction_diagnostic"

        # 3. disease_diagnosis
        disease_words = [
            "pythium", "rot", "rot", "disease", "mold", "fungus", "yellow", 
            "chlorosis", "pale", "tipburn", "tip burn", "dieback", "spots", "brown roots"
        ]
        if any(re.search(r'\b' + re.escape(w) + r'\b', clean_msg) for w in disease_words):
            return "disease_diagnosis"

        # 4. nutrient_management
        nutrient_words = [
            "ec", "ph", "tds", "ppm", "nutrient", "solution", "feeding", 
            "dosing", "concentration", "electrical conductivity", "water acidity"
        ]
        if any(re.search(r'\b' + re.escape(w) + r'\b', clean_msg) for w in nutrient_words) and \
           any(re.search(r'\b(?:mix|ppm|ec|ph|add|ratio|nutrient|dose)\b', clean_msg) for w in ["ppm", "ec", "ph"]):
            return "nutrient_management"

        # 5. yield_improvement
        yield_words = ["maximize", "increase", "yield", "improve yield", "more weight", "grow faster", "better size", "optimize yield"]
        if any(re.search(r'\b' + re.escape(w) + r'\b', clean_msg) for w in yield_words):
            return "yield_improvement"

        # 6. growth_stages
        stages_keywords = ["stage", "stages", "phase", "phases", "cycle", "cycles", "germination", "nursery", "vegetative", "harvest"]
        if any(re.search(r'\b' + re.escape(w) + r'\b', clean_resolved) for w in stages_keywords):
            return "growth_stages"

        # 7. parameter_insight
        param_words = ["ph", "ec", "co2", "humidity", "rh", "air temp", "water temp", "temperature"]
        if any(re.search(r'\b' + re.escape(w) + r'\b', clean_resolved) for w in param_words):
            return "parameter_insight"

        # 8. growth_optimization
        optimize_keywords = ["improve", "increase", "grow", "better", "maximize", "optimize", "more weight"]
        if any(re.search(r'\b' + re.escape(w) + r'\b', clean_resolved) for w in optimize_keywords):
            return "growth_optimization"

        # 9. general_hydroponics
        general_words = [
            "dwc", "nft", "hydroponics", "grow-room", "deep water", "nutrient film", 
            "oxygen", "aeration", "lighting", "dli", "led", "reservoir", "ventilation"
        ]
        if any(re.search(r'\b' + re.escape(w) + r'\b', clean_msg) for w in general_words):
            return "general_hydroponics"

        # 10. common_problems
        if "problem" in clean_resolved or "issue" in clean_resolved or "trouble" in clean_resolved:
            return "common_problems"

        # 11. knowledge_finder
        from backend.rag.retriever import retrieve
        retrieved_chunks = retrieve(message, top_k=3)
        if retrieved_chunks and retrieved_chunks[0].get("score", 0.0) > 0.08:
            return "knowledge_finder"

        # 12. fallback
        return "fallback"
