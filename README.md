# ESP Thermostat

Yet another ESP Thermostat implementation. Hopefully cooler than all the previous ones that you've seen. If not, please, let me know in the issues of this repository. It's gonna be truly appreciated.

## Goal

Create controller for electric heating unit that will turn on and off the heating and report the room temperature.

## Features overview

Don't bash me, it's just my wishlist, not based on user research, sorry.

### Done

Hopefully this list will soon start growing.

### To be done

- OTA Updates
- Relay controls
- Temperature telemetry
- Setup guide (Wi-FI Hot-spot for setup)
- MQTT Communication

## Firmware

I'm using cheap copy of NodeMCU with ESP8266.

Used firmware: https://micropython.org/resources/firmware/esp8266-20220618-v1.19.1.bin

### How to flash

First we install prerequisites.

```bash
# Assuming you have some version of Python3
pip install esptool

#Verify install
esptool.py -h
```

```bash
esptool.py --port <PORT> erase_flash

esptool.py --port <PORT> write_flash --flash_size=detect -fm dio 0x00000 <BIN_PATH>
```

## Misc

I'm using Thonny because it's super simple and gets me right to coding.

```
pip install thonny

thonny
```
