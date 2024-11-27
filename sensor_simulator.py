import time
import json
import random
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/temperature"

def simulate_sensor_data():
    client = mqtt.Client()
    client.connect(BROKER, PORT)

    while True:
        # Simulated temperature value
        # We have kept range from 26 so that the alarm is hit which is 28
        temperature = round(random.uniform(26.0, 30.0), 2)
        data = {
            "sensor": "temperature",
            "value": temperature,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
        }

        client.publish(TOPIC, json.dumps(data))
        print(f"Published: {data}")
        # Frequency after which data is published
        time.sleep(5)

if __name__ == "__main__":
    simulate_sensor_data()
