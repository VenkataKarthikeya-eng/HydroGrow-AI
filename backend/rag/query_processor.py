class QueryProcessor:
    """
    Handles query pre-processing and expansion to augment RAG search performance.
    """
    @staticmethod
    def expand_query(query: str, intent: str) -> str:
        clean_query = query.lower().strip()
        expanded_terms = []

        if intent == "disease_diagnosis":
            expanded_terms.extend(["treatment", "symptom", "prevention", "root infection", "pathogen", "solution"])
        elif intent == "nutrient_management":
            expanded_terms.extend(["ec value", "tds", "ppm range", "reservoir calibration", "dosing pumps", "macronutrients"])
        elif intent == "previous_prediction_analysis" or intent == "prediction_diagnostic":
            expanded_terms.extend(["predicted fresh weight", "growth category performance", "validation check", "crop yield"])
        elif intent == "yield_improvement" or intent == "growth_optimization":
            expanded_terms.extend(["maximize weight", "growth rate efficiency", "production targets", "dli photoperiod"])
        elif intent == "general_hydroponics":
            expanded_terms.extend(["dwc layout", "nft flow rate", "dissolved oxygen levels", "grow room setup"])

        if not expanded_terms:
            return clean_query

        # Combine original query with expansion tokens
        return f"{clean_query} {' '.join(expanded_terms)}"
