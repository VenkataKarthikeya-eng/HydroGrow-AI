import unittest
from backend.services.vision.growth_analyzer import GrowthAnalyzer

class TestGrowthAnalysis(unittest.TestCase):
    def test_analyze_seedling(self):
        res = GrowthAnalyzer().predict("lettuce_seedling.png")
        self.assertEqual(res["growth_stage"], "Seedling")
        self.assertLess(res["height_estimate"], 10.0)

    def test_analyze_vegetative(self):
        res = GrowthAnalyzer().predict("lettuce_vegetative.jpg")
        self.assertEqual(res["growth_stage"], "Vegetative")

    def test_analyze_harvest_ready(self):
        res = GrowthAnalyzer().predict("ready_to_harvest.png")
        self.assertEqual(res["growth_stage"], "Harvest Ready")
        self.assertGreater(res["leaf_area_estimate"], 300.0)
