# IoT Alarm System with MQTT and MongoDB

## **Overview**
This project simulates sensor data, listens to it using MQTT, and triggers alarms based on specific rules stored in a MongoDB database. The alarms are then published to an MQTT topic and logged in MongoDB for further processing or analysis.

---

## **Architecture and Components**

1. **Sensor Simulator**: 
   - Simulates sensor data (temperature in this case) and publishes it to the MQTT broker (`localhost`).
   
2. **MQTT Broker**:
   - Mosquitto MQTT broker running on localhost. It acts as a communication hub between the sensor simulator and the alarm service.
   
3. **Alarm Service**:
   - Listens for sensor data from MQTT topics (`sensors/#`).
   - Evaluates the data against predefined alarm rules stored in MongoDB.
   - If conditions are met, publishes alarms to a specific MQTT topic and logs them in MongoDB.

4. **MongoDB**:
   - **AlarmRules** collection: Stores rules for triggering alarms based on sensor data.
   - **State** collection: Stores the state of each alarm rule, including whether it is active and the start time of the alarm.
   - **AlarmLogs** collection: Stores the logs of triggered alarms for historical analysis.

---

## **Flow Diagram**

### **Diagram Description**
1. **Sensor Simulator**: 
   - Simulates temperature sensor data.
   - Publishes data to `sensors/temperature` topic on MQTT.

2. **MQTT Broker (Mosquitto)**:
   - Receives and distributes messages between the sensor simulator and alarm service.

3. **Alarm Service**: 
   - Listens to the `sensors/#` topic for incoming sensor data.
   - When new data arrives, it evaluates the data based on stored alarm rules in MongoDB.
     - **If an alarm condition is met**:
       - Publishes an alarm message to `alarms/temp_alarm` topic.
       - Logs the alarm in the `AlarmLogs` collection in MongoDB.
   - **If condition is not met**:
     - Updates the state of the alarm in the `State` collection to inactive.

---

## **Flowchart of the System**

![alt text](architecture.png)

## **Database commands**

![alt text](db.png)

![alt text](db_rule.png)

