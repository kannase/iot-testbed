# 🌐 IoT Device Automation Framework
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Robot Framework](https://img.shields.io/badge/robot%20framework-002E57?style=for-the-badge&logo=robotframework&logoColor=white) ![MQTT](https://img.shields.io/badge/MQTT-3C3C3C?style=for-the-badge&logo=mqtt&logoColor=white) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

This project demonstrates a professional-grade test automation framework for an **IoT Ecosystem**, featuring a simulated **IoT Device** communicating via **MQTT** and a suite of tests built with **Robot Framework**.

## 🏗️ Architecture: "IoT Device"
The project uses a generic **"IoT Device" architecture** to demonstrate scalability:
* **Namespace Standardization**: Uses a root namespace (`iot/device/telemetry`) for easy expansion.
* **Separation of Concerns**: Simulator (`simulator/`) and Test Suite (`tests/`) are kept independent.
* **Hybrid Simulation**: Functions as a standalone process and an importable Python library.

## 🧪 Automated Test Suite
The framework includes two critical layers of testing:
### 1. Infrastructure Validation (Smoke Test)
**Test Case:** `Self Communication Test` 
* **Purpose**: Validates the health of the MQTT Broker (Mosquitto). 
* **Mechanism**: Publishes a unique string (`HELLO_BROKER`) and verifies reception. 

### 2. Functional Business Logic Test
**Test Case:** `Verify Device Logic With Custom Keyword` 
* **Purpose**: Validates "Air Quality" reporting based on CO2 sensor data. 
* **Custom Python Integration**: Uses a helper, `get_latest_mqtt_message`, to solve asynchronous timing issues. 
* **Logic Verification**: Verifies if `co2_level < 1000` is `SAFE`, otherwise `DANGER`. 

## 🚀 Getting Started
### Prerequisites
* Python 3.x
* Mosquitto MQTT Broker
* Dependencies: `pip install -r requirements.txt`

### Running the Project
1. **Start Simulator**: `python simulator/iot_device_simulator.py`
2. **Run Tests**: `robot tests/iot_integration_test.robot`
