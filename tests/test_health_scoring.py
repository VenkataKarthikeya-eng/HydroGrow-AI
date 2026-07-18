import unittest
from backend.services.vision.health_scoring import HealthScoring

class TestHealthScoring(unittest.TestCase):
    def test_healthy_score(self):
        disease = {"disease": "Healthy", "severity": "None"}
        growth = {"growth_score": 90.0}
        score = HealthScoring.calculate_health_score(disease, growth)
        self.assertGreaterEqual(score, 90.0)

    def test_severe_disease_deduction(self):
        disease = {"disease": "Root Rot Symptoms", "severity": "High"}
        growth = {"growth_score": 90.0}
        score = HealthScoring.calculate_health_score(disease, growth)
        self.assertLess(score, 50.0)
