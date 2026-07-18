import unittest
from backend.cloud.mqtt_service import MQTTService

class TestMQTTService(unittest.TestCase):

    def test_mqtt_connect_and_parse(self):
        mqtt = MQTTService()
        res = mqtt.connect_device("ESP32_001")
        self.assertEqual(res["status"], "connected")

        payload = {
            "device_id": "ESP32_001",
            "temperature": 24.5,
            "humidity": 70,
            "water_ph": 6.1,
            "water_ec": 1.8
        }
        parsed = mqtt.receive_sensor_data(payload)
        self.assertEqual(parsed["device_id"], "ESP32_001")
        self.assertEqual(parsed["temperature"], 24.5)
        self.assertEqual(parsed["water_ph"], 6.1)

if __name__ == "__main__":
    unittest.main()
