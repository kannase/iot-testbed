# iot-testbed
A Local Functional Test Bed for IoT telemetry, featuring a Python-based Pod simulator, MQTT protocol integration, and automated validation using Robot Framework and Pytest.
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Robot Framework](https://img.shields.io/badge/Robot%20Framework-6.1-brightgreen.svg)
![MQTT](https://img.shields.io/badge/Protocol-MQTT-orange.svg)

## 📋 Features
- **Digital Twin:** Python-based simulator for real-time sensor data.
- **Async Communication:** MQTT protocol integration via Mosquitto.
- **Automated Validation:** Test suites built in Robot Framework and Pytest.

## 🛠️ Setup Instructions
1. Install requirements: `pip install -r requirements.txt`
2. Start the MQTT Broker (Mosquitto).
3. Run the simulator: `python simulator/jsondata.py`
4. Run tests: `robot tests/`
