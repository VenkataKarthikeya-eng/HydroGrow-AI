# HydroGrow AI IoT Hardware Setup & Integration Guide

Instructions for configuring ESP32, Raspberry Pi, and Arduino hardware nodes to stream sensor telemetry to HydroGrow AI.

---

## 1. Hardware Pin & Sensor Mapping

- **ESP32 Node Setup:**
  - `GPIO 34`: Analog Water pH Sensor
  - `GPIO 35`: Analog Water EC/TDS Sensor
  - `GPIO 32`: DS18B20 Water Temperature Sensor
  - `GPIO 33`: DHT22 Air Temperature & Humidity Sensor
  - `GPIO 25`: NDIR CO2 Sensor (UART RX/TX)

---

## 2. Hardware Registration & Provisioning

1. Navigate to **Cloud Ops** (`/cloud`) on the HydroGrow AI dashboard.
2. Click **Provision Device** and specify `Device ID` (e.g. `ESP32_001`).
3. Copy the generated `Hardware API Access Key` (`hg_key_...`).
4. Program the key into your microcontroller firmware header file (`config.h`).

---

## 3. Sample ESP32 C++ Code Snippet

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://your-server-ip:8000/api/devices/ESP32_001/telemetry";
const char* apiKey = "hg_key_your_generated_access_key";

void sendTelemetry() {
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-API-Key", apiKey);

  StaticJsonDocument<200> doc;
  doc["device_id"] = "ESP32_001";
  doc["water_ph"] = 6.15;
  doc["water_ec"] = 1.85;
  doc["temperature"] = 24.5;
  doc["humidity"] = 68.0;

  String jsonPayload;
  serializeJson(doc, jsonPayload);
  int httpCode = http.POST(jsonPayload);
  http.end();
}
```
