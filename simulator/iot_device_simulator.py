import paho.mqtt.client as mqtt
import time
import random
import argparse

# --- Configuration ---
parser = argparse.ArgumentParser()
parser.add_argument('--broker', type=str, default='localhost', help='MQTT broker hostname')
args = parser.parse_args()

BROKER = args.broker
PORT = 1883
TOPIC = "home/sensor/temperature"

def run_simulator():
    client = mqtt.Client()
    
    retry_count = 0
    max_retries = 5
    connected = False

    while retry_count < max_retries:
        try:
            print(f"Connecting to broker {BROKER} (Attempt {retry_count + 1}/{max_retries})...")
            client.connect(BROKER, PORT)
            connected = True
            print("Successfully connected to the broker!")
            break
        except Exception as e:
            retry_count += 1
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    if not connected:
        print("ERROR: Could not connect to MQTT broker.")
        exit(1)

    client.loop_start()

    try:
        print(f"Starting to publish data to {TOPIC}...")
        # BACK TO FOREVER MODE
        while True:
            temp = round(random.uniform(18.0, 26.0), 2)
            client.publish(TOPIC, temp)
            print(f"Published: {temp} to {TOPIC}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        print("Cleaning up...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    run_simulator()