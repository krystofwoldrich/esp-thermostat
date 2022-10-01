# https://randomnerdtutorials.com/micropython-esp32-esp8266-dht11-dht22-web-server/
# With changes but the core remains the same

try:
  import usocket as socket
except:
  import socket

import network
from machine import Pin

import esp
esp.osdebug(None)

import gc
gc.collect()

import dht

def get_config():
    config = {}
    file = open('config', 'r')
    for line in file:
        raw = line.split('=', 1)
        config[raw[0].strip()]=raw[1].strip()
    file.close()
    return config

config = get_config()

sensor = dht.DHT22(Pin(int(config['sensor'])))

ssid = config['ssid']
password = config['password']

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())
