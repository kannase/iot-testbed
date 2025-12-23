import paho.mqtt.client as mqtt
import time
import random
import json

def get_latest_mqtt_message(lib_instance, topic):
    """Helper for Robot Framework to parse messages."""
    buffer = getattr(lib_instance, '_messages', {})
    messages = buffer.get(topic, [])
    return messages[-1] if messages else None

def run_simulator():
    BROKER = "localhost"
    TOPIC = "framery/pods/status"
    # Using Paho 1.6 compatible client initialization
    client = mqtt.Client("Pod_Simulator_001")
    client.connect(BROKER, 1883)
    
    print(f"Simulator started. Publishing to {TOPIC}...")
    
    try:
        while True:
            co2 = random.randint(400, 1200)
            status = "SAFE" if co2 < 1000 else "DANGER"
            pod_data = {
                "device_id": "TAMPERE-POD-01", 
                "co2_level": co2, 
                "air_quality": status
            }
            
            # The informative print logic from your 'version_2'
            print(f"Sent: {status} | CO2: {co2}") 
            
            client.publish(TOPIC, json.dumps(pod_data))
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\nShutting down simulator...")
        client.disconnect()

if __name__ == "__main__":
    run_simulator()
