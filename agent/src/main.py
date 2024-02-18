from paho.mqtt import client as mqtt_client
import json
import time
from schema.aggregated_data_schema import AccelerometerSchema, GpsSchema, ParkingSchema
from file_datasource import FileDatasource
import config


def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)  # Stop execution

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def publish(client, topic, data, schema):
    """Publish data to MQTT topic"""
    msg = schema.dumps(data)
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        pass
    else:
        print(f"Failed to send message to topic {topic}")


def run():
    # Prepare MQTT client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)

    # Prepare datasource
    datasource = FileDatasource("data/accelerometer.csv", "data/gps.csv", "data/parking.csv")
    datasource.startReading()

    while True:
        # Read data from datasource
        data = datasource.read()

        # Publish accelerometer data to MQTT topic
        publish(client, config.MQTT_ACCELEROMETER_TOPIC, data.accelerometer, AccelerometerSchema())

        # Publish gps data to MQTT topic
        publish(client, config.MQTT_GPS_TOPIC, data.gps, GpsSchema())

        # Publish parking data to MQTT topic
        publish(client, config.MQTT_PARKING_TOPIC, data.parking, ParkingSchema())

        time.sleep(config.DELAY)



if __name__ == "__main__":
    run()