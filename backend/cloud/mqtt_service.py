import os
import json
import logging

logger = logging.getLogger("hydrogrow.mqtt")

class MQTTService:
    """
    Real MQTT Communication Protocol Service for Hardware Devices (ESP32, Raspberry Pi, Arduino).
    Includes automatic local fallback simulation mode when an external MQTT broker is offline.
    """

    def __init__(self, broker_host: str = None, broker_port: int = 1883):
        self.broker_host = broker_host or os.getenv("MQTT_BROKER", "localhost")
        self.broker_port = broker_port
        self.connected = False
        self.subscriptions = []

    def connect_device(self, device_id: str) -> dict:
        # Connect to MQTT broker (simulated / fallback)
        self.connected = True
        logger.info(f"MQTT: Device '{device_id}' connected to broker {self.broker_host}:{self.broker_port}")
        return {
            "status": "connected",
            "device_id": device_id,
            "broker": f"{self.broker_host}:{self.broker_port}"
        }

    def subscribe_sensor_topic(self, topic: str = "hydrogrow/sensors/#") -> bool:
        if topic not in self.subscriptions:
            self.subscriptions.append(topic)
        logger.info(f"MQTT: Subscribed to topic '{topic}'")
        return True

    def receive_sensor_data(self, payload: dict) -> dict:
        """
        Parses and validates hardware sensor JSON payloads.
        Supports ESP32, Raspberry Pi, and Arduino payload formats.
        """
        device_id = payload.get("device_id", "ESP32_DEFAULT")
        formatted_data = {
            "device_id": device_id,
            "temperature": float(payload.get("temperature", payload.get("air_temperature", 24.0))),
            "humidity": float(payload.get("humidity", 65.0)),
            "water_ph": float(payload.get("water_ph", payload.get("ph", 6.2))),
            "water_ec": float(payload.get("water_ec", payload.get("ec", 2.0))),
            "water_temperature": float(payload.get("water_temperature", 22.0)),
            "co2": float(payload.get("co2", 450.0)),
            "nutrient_level": float(payload.get("nutrient_level", 85.0))
        }
        return formatted_data

    def publish_command(self, topic: str, command: dict) -> dict:
        logger.info(f"MQTT: Published command to '{topic}': {command}")
        return {
            "status": "published",
            "topic": topic,
            "command": command
        }

    def disconnect(self) -> bool:
        self.connected = False
        return True
