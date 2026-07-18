import logging

logger = logging.getLogger(__name__)

# Simulated device statuses in memory
DEVICE_STATES = {
    "Nutrient Pump": "inactive",
    "pH Controller": "inactive",
    "Water Pump": "inactive",
    "Cooling Fan": "inactive",
    "Grow Lights": "active",
    "Ventilation System": "active"
}

class ActionSimulator:
    """
    Stub simulator representing virtual greenhouse relays (actuators),
    intercepting control demands safely in simulation mode.
    """
    @staticmethod
    def simulate_action(device: str, action_type: str, action_value: str) -> dict:
        if device not in DEVICE_STATES:
            return {"device": device, "status": "unknown", "reason": "Unknown hardware asset"}

        status = "activated" if action_type == "activate" else "deactivated"
        DEVICE_STATES[device] = "active" if action_type == "activate" else "inactive"
        
        logger.info(f"Hardware Simulator: [{device}] transition to status: {status}")

        return {
            "device": device,
            "status": status,
            "reason": f"Simulated {action_type} action ({action_value})"
        }

    @staticmethod
    def get_device_status(device: str) -> str:
        return DEVICE_STATES.get(device, "unknown")
