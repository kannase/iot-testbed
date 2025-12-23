import paho.mqtt.client as mqtt
import time
import random
import json

def get_latest_mqtt_message(lib_instance, topic):
    """Helper for Robot Framework to parse messages from the internal buffer."""
    buffer = getattr(lib_instance, '_messages', {})
    messages = buffer.get(topic, [])
    return messages[-1] if messages else None

def run_simulator():
    # Generic IoT Topic Structure
    BROKER = "localhost"
    TOPIC = "iot/device/telemetry"
    
    # Client Setup (Paho 1.6 compatible)
    client = mqtt.Client("IoT_Gateway_001")
    client.connect(BROKER, 1883)
    
    print(f"--- IoT Device Simulator Started ---")
    print(f"Publishing to: {TOPIC}\n")
    
    try:
        while True:
            co2 = random.randint(400, 1200)
            status = "SAFE" if co2 < 1000 else "DANGER"
            
            payload_data = {
                "device_id": "SENSOR-01", 
                "co2_level": co2, 
                "air_quality": status,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            
            # Hybrid logging: Professional but visible
            print(f"Sent: {status} | CO2: {co2} ppm") 
            
            client.publish(TOPIC, json.dumps(payload_data))
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\nShutting down...")
        client.disconnect()

if __name__ == "__main__":
    run_simulator()
