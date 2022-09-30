import dht
from machine import Pin
from time import sleep

sensor = dht.DHT22(Pin(4))
led = Pin(2, Pin.OUT)
while True:
    led.value(0)
    sleep(0.5)
    led.value(1)
    sleep(0.5)
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        temp_f = temp * (9/5) + 32.0
        print('Temperature: %3.1f C' %temp)
        print('Temperature: %3.1f F' %temp_f)
        print('Humidity: %3.1f %%' %hum)
    except OSError as e:
        print('Failed to read sensor.')
