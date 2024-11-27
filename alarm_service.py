from db_utils import get_db
from datetime import datetime, timedelta
import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
SUBSCRIBE_TOPIC = "sensors/#"
db = get_db()

# MQTT clients
listener_client = mqtt.Client()
publisher_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(SUBSCRIBE_TOPIC)


def on_message(client, userdata, message):
    # Process incoming data from the sensor and evaluate alarms.
    try:
        sensor_data = json.loads(message.payload)
        print(f"Received: {sensor_data}")
        evaluate_alarm(sensor_data)
    except Exception as e:
        print(f"Error processing message: {e}")


def evaluate_alarm(sensor_data):
    """Evaluate alarm rules against incoming sensor data."""
    rules = db["AlarmRules"].find({"sensor_id": sensor_data["sensor"]})
    for rule in rules:
        rule_id = rule["rule_id"]
        threshold = rule["threshold"]
        duration = rule["duration"]
        condition = rule["condition"]
        value = sensor_data["value"]

        # Evaluate condition
        if condition == "greater" and value > threshold:
            now = datetime.now()
            state = db["State"].find_one({"rule_id": rule_id})

            if state and state["is_active"]:
                start_time = datetime.fromisoformat(state["start_time"])
                if now - start_time > timedelta(seconds=duration):
                    publish_alarm(sensor_data, rule)
            else:
                # Saving the state in DB
                db["State"].update_one(
                    {"rule_id": rule_id},
                    {"$set": {"start_time": now.isoformat(), "is_active": True}},
                    upsert=True
                )
        else:
            # Deactivate the state if condition is not met
            db["State"].update_one(
                {"rule_id": rule_id},
                {"$set": {"is_active": False}},
                upsert=True
            )


def publish_alarm(sensor_data, rule):
    #Publish alarm to MQTT and will log in MongoDB.
    alarm_data = {
        "rule_id": rule["rule_id"],
        "sensor": sensor_data["sensor"],
        "value": sensor_data["value"],
        "timestamp": sensor_data["timestamp"]
    }

    # Publish alarm data to the "alarms/temp_alarm"
    publisher_client.publish(rule["output_topic"], payload=json.dumps(alarm_data))
    print(f"Alarm Published to {rule['output_topic']}: {alarm_data}")

    # Saving the data in MongoDB
    db["AlarmLogs"].insert_one(alarm_data)


if __name__ == "__main__":
    listener_client.on_connect = on_connect
    listener_client.on_message = on_message
    listener_client.connect(BROKER, PORT)

    publisher_client.connect(BROKER, PORT)

    # Start the MQTT listener
    listener_client.loop_forever()
