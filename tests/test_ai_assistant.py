"""
test_ai_assistant.py — Unit Tests for Conversational AI Assistant Layer

This test script validates the conversational AI assistant:
1. Question understanding (intent matching for pH, EC, growth stages, diseases).
2. Prediction context usage (dynamic answering for prediction bottlenecks like low pH or low CO2).
3. Empty input handling (whitespace queries receive helpful prompts).
4. Fallback messaging for unrelated questions.
"""

import sys
import os
import unittest

# Try to reconfigure stdout to UTF-8 to prevent UnicodeEncodeErrors with emojis on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Ensure the project root folder is in the python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(BASE_DIR, "..")))

from backend.services.intelligence.ai_assistant import HydroGrowAssistant


class TestAIAssistant(unittest.TestCase):
    
    def setUp(self):
        self.assistant = HydroGrowAssistant()
        
        # Setup mock context
        self.context = {
            "user_inputs": {
                "water_ph": 4.5,            # Low pH
                "water_ec": 2.0,
                "water_tds": 1.0,
                "water_temperature": 21.0,
                "air_temperature": 22.0,
                "humidity": 60.0,
                "co2": 350.0,               # Low CO2
                "nutrient_solution_ml": 400.0,
                "water_consumption_l": 170.0,
                "acid_consumption_ml": 40.0,
                "initial_height_cm": 12.0,
                "initial_weight_g": 4.0,
                "initial_root_length_cm": 7.0,
            },
            "prediction_result": {
                "prediction_value": 377.25,
                "growth_category": "🌟 Excellent",
                "was_adjusted": True,
                "validation_message": "Prediction was outside biological range and was corrected."
            },
            "recommendation_outputs": [
                {
                    "type": "critical",
                    "parameter": "Water pH",
                    "value": "4.5",
                    "status": "Critical",
                    "message": "Water pH is critically low (< 5.0). Extreme acidity damages root tissues...",
                    "action": "Immediately add pH-up solution."
                },
                {
                    "type": "warning",
                    "parameter": "CO2 Level",
                    "value": "350 ppm",
                    "status": "Warning",
                    "message": "CO2 is low...",
                    "action": "Increase ventilation or supplement with CO2."
                }
            ],
            "explanation_output": {
                "summary": "HydroGrow AI predicts 377.2g fresh weight. The crop performance is classified as Excellent.",
                "positive_factors": [
                    {"factor": "Water EC", "impact": "positive", "explanation": "EC (2.00 mS/cm) is optimal."}
                ],
                "improvement_opportunities": [
                    {"factor": "Water pH", "impact": "improvement", "explanation": "Water pH (4.5) is critically low, causing root damage (root burn)."},
                    {"factor": "CO2 Level", "impact": "improvement", "explanation": "CO2 level is below the ideal productivity range."}
                ],
                "confidence_explanation": "Based on 216 samples."
            }
        }

    def test_empty_input_handling(self):
        """Verify that empty queries or whitespace return a prompt to ask a question."""
        res_empty = self.assistant.get_response("", self.context)
        self.assertIn("type a question", res_empty.lower())

        res_space = self.assistant.get_response("   ", self.context)
        self.assertIn("type a question", res_space.lower())

    def test_prediction_context_usage(self):
        """Verify that questions about prediction weight incorporate active bottlenecks from context."""
        query = "Why is my prediction only 377g?"
        res = self.assistant.get_response(query, self.context)
        
        # Assert active bottlenecks are referenced
        self.assertIn("Water pH", res)
        self.assertIn("CO2 Level", res)
        self.assertIn("root damage", res)
        self.assertIn("Immediately add pH-up solution", res)

    def test_optimization_advice(self):
        """Verify that questions about improving growth return categorized advice based on context."""
        query = "How can I improve my growth?"
        res = self.assistant.get_response(query, self.context)
        
        self.assertIn("Growth Optimization Advice", res)
        self.assertIn("Water & Nutrient Improvements", res)
        self.assertIn("Environmental Improvements", res)
        self.assertIn("Immediately add pH-up solution", res)

    def test_parameter_inquiries(self):
        """Verify that parameter questions return optimal ranges and current statuses."""
        query = "What is the optimal range for water pH?"
        res = self.assistant.get_response(query, self.context)
        
        self.assertIn("Parameter Insight: Water pH", res)
        self.assertIn("Ideal Range", res)
        self.assertIn("5.5", res)
        self.assertIn("Current Value", res)
        self.assertIn("4.5", res)
        self.assertIn("Status: **Critical**", res)

    def test_problem_troubleshooting(self):
        """Verify that common problem inquiries fetch correct diagnosis and solutions."""
        query = "How do I solve tip burn?"
        res = self.assistant.get_response(query, self.context)
        
        self.assertIn("Agricultural Problem: Tip Burn", res)
        self.assertIn("Calcium deficiency in growing tips", res)
        self.assertIn("Reduce humidity to 50-60%", res)

    def test_growth_stages(self):
        """Verify that inquiries about growth stages return the correct phases sequence."""
        query = "Show me the growth stages"
        res = self.assistant.get_response(query, self.context)
        
        self.assertIn("Lettuce Growth Phases", res)
        self.assertIn("Germination", res)
        self.assertIn("Nursery Stage", res)
        self.assertIn("Vegetative Phase", res)
        self.assertIn("Harvest Stage", res)

    def test_fallback_response(self):
        """Verify that unrelated inputs return a clean fallback detailing assistant options."""
        query = "What is the capital of Japan?"
        res = self.assistant.get_response(query, self.context)
        
        self.assertIn("HydroGrow AI Assistant", res)
        self.assertIn("optimize hydroponic settings", res)
        self.assertIn("Why is my predicted growth low?", res)


if __name__ == "__main__":
    unittest.main()
