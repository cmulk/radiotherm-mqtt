from myradiotherm import CT50
import paho.mqtt.client as mqtt
import signal
import sys
from time import sleep
import json

DEVICE_NAME="home"
TSTAT_IP = "radiotherm.lan"
ID="myradiotherm1"

MQTT_ID = "local_therm"
BROKER = "<<my_broker>>"
PORT = 1883
USERNAME = "<<mqtt_username>>"
PASSWORD = "<<mqtt_password>>"


STATUS_TOPIC = "climate/stat/{0}/status".format(DEVICE_NAME)
SET_TEMP = "climate/cmnd/{0}/settemp".format(DEVICE_NAME)
SET_MODE = "climate/cmnd/{0}/setmode".format(DEVICE_NAME)
SET_FAN = "climate/cmnd/{0}/setfan".format(DEVICE_NAME)
SET_HOLD = "climate/cmnd/{0}/sethold".format(DEVICE_NAME)
AVAILABLE_TOPIC = "climate/tele/{0}/available".format(DEVICE_NAME)



def end_well(signum, stackframe):
    print("Stopping MQTT loop...")
    client.publish(AVAILABLE_TOPIC, "offline", retain=False)
    client.disconnect()
    client.loop_stop()
    sys.exit()


def on_log(client, userdata, level, buf):
    print("mqtt: ", buf)


def on_connect(client, userdata, flags, rc):
    client.subscribe(SET_TEMP)
    client.subscribe(SET_MODE)
    client.subscribe(SET_FAN)
    client.subscribe(SET_HOLD)
    client.message_callback_add(SET_TEMP, on_set_temp)
    client.message_callback_add(SET_MODE, on_set_mode)
    client.message_callback_add(SET_FAN, on_set_fan)
    client.message_callback_add(SET_HOLD, on_set_hold)


def on_set_temp(client, userdata, msg):
    tstat.set_temp(msg.payload.decode())
    client.publish(STATUS_TOPIC, json.dumps(tstat.current_stat), retain=False)
    print(repr(tstat.current_stat))

def on_set_mode(client, userdata, msg):
    tstat.set_mode(msg.payload.decode())
    client.publish(STATUS_TOPIC, json.dumps(tstat.current_stat), retain=False)
    print(repr(tstat.current_stat))

def on_set_fan(client, userdata, msg):
    tstat.set_fan(msg.payload.decode())
    client.publish(STATUS_TOPIC, json.dumps(tstat.current_stat), retain=False)
    print(repr(tstat.current_stat))

def on_set_hold(client, userdata, msg):
    tstat.set_hold(msg.payload.decode())
    client.publish(STATUS_TOPIC, json.dumps(tstat.current_stat), retain=False)
    print(repr(tstat.current_stat))

#############################################
###### MAIN ######
#############################################

signal.signal(signal.SIGINT, end_well)
signal.signal(signal.SIGTERM, end_well)


client = mqtt.Client(client_id=MQTT_ID)
#client.on_log = on_log
client.username_pw_set(USERNAME, PASSWORD)
client.will_set(AVAILABLE_TOPIC, "offline")
client.on_connect = on_connect
client.connect(BROKER, port=PORT)
client.loop_start()

tstat = CT50(therm_address = TSTAT_IP)

while True:
    
    client.publish(AVAILABLE_TOPIC, "online", retain=False)
    client.publish(STATUS_TOPIC, json.dumps(tstat.current_stat), retain=False)
    sleep(60)
    tstat.update_status()
