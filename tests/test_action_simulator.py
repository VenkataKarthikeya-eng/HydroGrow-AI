import unittest
from backend.services.automation.action_simulator import ActionSimulator

class TestActionSimulator(unittest.TestCase):
    def test_simulate_device_states(self):
        # 1. Test invalid device returns unknown status
        res = ActionSimulator.simulate_action("Invalid Actuator", "activate", "some_value")
        self.assertEqual(res["status"], "unknown")

        # 2. Test activate state transitions
        res = ActionSimulator.simulate_action("Cooling Fan", "activate", "Critical Temp Correction")
        self.assertEqual(res["status"], "activated")
        self.assertEqual(ActionSimulator.get_device_status("Cooling Fan"), "active")

        # 3. Test deactivate transitions
        res = ActionSimulator.simulate_action("Cooling Fan", "deactivate", "Correction Finished")
        self.assertEqual(res["status"], "deactivated")
        self.assertEqual(ActionSimulator.get_device_status("Cooling Fan"), "inactive")
