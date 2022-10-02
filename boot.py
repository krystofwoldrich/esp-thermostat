# https://randomnerdtutorials.com/micropython-esp32-esp8266-dht11-dht22-web-server/
# With changes but the core remains the same

try:
    import usocket as socket
except:
    import socket
import network
from machine import Pin
import esp
import gc
import dht
from umqttsimple import MQTTClient
import ubinascii
import machine


def get_config():
    config = {}
    file = open("config", "r")
    for line in file:
        if len(line.strip()) > 0:
            raw = line.split("=", 1)
            config[raw[0].strip()] = raw[1].strip()
    file.close()
    return config


def save_config(config):
    file = open("config", "w")
    raw = ""
    for key in config:
        raw += key + "=" + config[key] + "\n"
    file.write(raw)
    file.close()


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("network config:", wlan.ifconfig())


def setup_mqtt(config):
    id = machine.unique_id()
    client_id = ubinascii.hexlify(id)
    config["client_id"] = client_id


esp.osdebug(None)
gc.collect()

config = get_config()
sensor = dht.DHT22(Pin(int(config["sensor"])))

ssid = config["ssid"]
password = config["password"]
connect_wifi(ssid, password)

setup_mqtt(config)

print("Boot complete")
