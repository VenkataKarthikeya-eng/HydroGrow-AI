"""
test_phase7_ai_system.py — Unit Tests for Advanced RAG and AI Assistant Subsystem

This test script validates Phase 7 upgrades:
1. Retrieval accuracy and TF-IDF scoring.
2. Retrieval response time performance (must run under 1.0s).
3. Prediction context integration.
4. Conversation memory and follow-up query resolution.
5. Professional formatted responses (Analysis, Evidence, Recommendation).
6. Expanded knowledge base query mapping.
7. Unrelated fallback handling.
"""

import sys
import os
import time
import unittest

# Ensure the project root folder is in the python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(BASE_DIR, "..")))

from backend.services.intelligence.ai_assistant import HydroGrowAssistant
from backend.rag.retriever import retrieve


class TestPhase7AISystem(unittest.TestCase):
    
    def setUp(self):
        self.assistant = HydroGrowAssistant()
        
        # Setup mock dashboard context
        self.context = {
            "user_inputs": {
                "water_ph": 4.5,            # Critical low pH
                "water_ec": 1.0,            # Low EC
                "water_tds": 0.5,
                "water_temperature": 25.0,  # Warm water
                "air_temperature": 22.0,
                "humidity": 60.0,
                "co2": 450.0,
                "nutrient_solution_ml": 400.0,
                "water_consumption_l": 170.0,
                "acid_consumption_ml": 40.0,
                "initial_height_cm": 12.0,
                "initial_weight_g": 4.0,
                "initial_root_length_cm": 7.0,
            },
            "prediction_result": {
                "prediction_value": 245.5,
                "growth_category": "Poor",
                "was_adjusted": False,
                "validation_message": "Prediction is within realistic bounds."
            },
            "recommendation_outputs": [
                {
                    "type": "critical",
                    "parameter": "Water pH",
                    "value": "4.5",
                    "status": "Critical",
                    "message": "pH is critical...",
                    "action": "Immediately add pH-up solution."
                },
                {
                    "type": "warning",
                    "parameter": "Water EC",
                    "value": "1.0 mS/cm",
                    "status": "Warning",
                    "message": "EC is warning...",
                    "action": "Increase nutrient concentration gradually."
                }
            ],
            "explanation_output": {
                "summary": "HydroGrow AI predicts 245.5g weight.",
                "positive_factors": [],
                "improvement_opportunities": [
                    {"factor": "Water pH", "explanation": "Water pH is critically low (4.5), causing root tissue damage."},
                    {"factor": "Water EC", "explanation": "EC is below optimal nutrient availability ranges."}
                ],
                "confidence_explanation": "Based on 216 samples."
            },
            "conversation_history": []
        }

    def test_knowledge_retrieval(self):
        """Verify that retriever fetches accurate and relevant chunks."""
        results = retrieve("tip burn", top_k=2)
        self.assertTrue(len(results) > 0)
        
        # Validate that the top result relates to tip burn or calcium
        top_content = results[0]["content"].lower()
        self.assertTrue("tip burn" in top_content or "calcium" in top_content)
        self.assertIsNotNone(results[0]["source"])

    def test_retrieval_performance(self):
        """Verify that local retriever runs in under 1.0 second."""
        start_time = time.time()
        for i in range(20):
            retrieve("nitrogen deficiency and water temp", top_k=3)
        duration = time.time() - start_time
        
        avg_time = duration / 20.0
        print(f"\n[INFO] Average retrieval response time: {avg_time * 1000:.2f} ms")
        self.assertLess(avg_time, 1.0, f"Retrieval average took too long: {avg_time}s")

    def test_context_usage(self):
        """Verify that dashboard prediction context merges with the query response."""
        query = "Why is my prediction low?"
        res = self.assistant.get_response(query, self.context)
        
        self.assertIn("Water pH", res)
        self.assertIn("Water EC", res)
        self.assertIn("Immediately add pH-up solution", res)

    def test_conversation_memory(self):
        """Verify follow-up queries reference previous questions using conversation history."""
        # 1. Setup conversation history where the previous message was about water pH
        self.context["conversation_history"] = [
            {"role": "user", "content": "Tell me about water pH"},
            {"role": "assistant", "content": "Water pH is optimal between 5.5 and 6.5."},
            {"role": "user", "content": "how do I adjust it?"} # Short ambiguous query referencing pH
        ]
        
        res = self.assistant.get_response("how do I adjust it?", self.context)
        
        # It should resolve 'it' to water pH and return pH-related recommendations
        self.assertIn("Water pH", res)
        self.assertIn("Ideal Range", res)
        self.assertIn("pH-up", res)
        self.assertIn("Follow-up context applied", res)

    def test_professional_format(self):
        """Verify response contains the structured Analysis, Evidence, and Recommendation tags."""
        res_ph = self.assistant.get_response("Explain pH", self.context)
        self.assertIn("🌱 **Analysis:**", res_ph)
        self.assertIn("📊 **Evidence:**", res_ph)
        self.assertIn("💡 **Recommendation:**", res_ph)

        res_prob = self.assistant.get_response("How to solve root rot?", self.context)
        self.assertIn("🌱 **Analysis:**", res_prob)
        self.assertIn("📊 **Evidence:**", res_prob)
        self.assertIn("💡 **Recommendation:**", res_prob)

    def test_expanded_knowledge(self):
        """Verify retriever maps queries to the expanded Phase 7 knowledge categories."""
        # Test lighting
        res_light = self.assistant.get_response("spectrum requirements", self.context)
        self.assertIn("spectrum", res_light.lower())
        self.assertIn("lighting_requirements", res_light)
        
        # Test DO
        res_do = self.assistant.get_response("dissolved oxygen target", self.context)
        self.assertIn("dissolved_oxygen_management", res_do)
        self.assertIn("oxygen", res_do.lower())

        # Test deficiencies
        res_def = self.assistant.get_response("magnesium deficiency symptoms", self.context)
        self.assertIn("nutrient_deficiencies/Magnesium", res_def)
        self.assertIn("interveinal chlorosis", res_def.lower())

        # Test mistakes
        res_mist = self.assistant.get_response("light leaks", self.context)
        self.assertIn("greenhouse_mistakes/Light Leaks in Reservoir", res_mist)
        self.assertIn("algae", res_mist.lower())

        # Test harvesting
        res_harv = self.assistant.get_response("flushing protocol before harvesting", self.context)
        self.assertIn("harvesting_optimization/flushing_protocol", res_harv)
        self.assertIn("nitrate", res_harv.lower())

    def test_fallback_handling(self):
        """Verify empty and unrelated inputs are handled gracefully."""
        res_empty = self.assistant.get_response("", self.context)
        self.assertIn("type a question", res_empty.lower())

        res_unrelated = self.assistant.get_response("What is the temperature on Mars?", self.context)
        self.assertIn("HydroGrow AI Assistant", res_unrelated)
        self.assertIn("optimize hydroponic settings", res_unrelated)


if __name__ == "__main__":
    unittest.main()
