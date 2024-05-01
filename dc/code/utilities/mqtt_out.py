"""mqtt_out.py

Working assumptions:
	- The broker and port will not change during a session, but the topic could.
	- The user would like a one-line interaction with the MQTT system

Public API: only the function 'publish'

"""
# installed imports
import paho.mqtt.client as pahomqttclient

# local imports
from utilities.timestamp import get_timestamp

# default settings
default_broker = "mqtt.docker.local"
default_topic = "shoestring-sensor"
default_port = 1883
#default_qos = 0                # qos not in use


# startup
client = pahomqttclient.Client()
client._is_connected = False    # create custom attribute

def _connect(broker, port):
    print("MQTT client connecting to", broker, port)
    client.connect(broker, port)
    client._is_connected = True # should test connection attempt was sucessful


def publish(msg, topic=default_topic, broker=default_broker, port=default_port):
    """Add timestamp to msg, connect (if not already) and publish. 
    Arg reordering is deliberate to allow kwargs.
    """

    # Get the timestamp first, as soon as possible after sampling
    timestamp = get_timestamp()

    if not client._is_connected:
        _connect(broker, port)

    payload = timestamp + " " + str(msg)
    client.publish(topic, payload)
