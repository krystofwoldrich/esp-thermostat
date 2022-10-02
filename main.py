# https://randomnerdtutorials.com/micropython-esp32-esp8266-dht11-dht22-web-server/
# With changes but the core remains the same

# https://github.com/swvincent/mp-web-non-blocking/blob/master/mp-web-non-blocking/main.py
# Non blocking web server implementation

import time
import machine
from uselect import select


def read_sensor():
    temp = hum = 0
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        if (isinstance(temp, float) and isinstance(hum, float)) or (
            isinstance(temp, int) and isinstance(hum, int)
        ):
            hum = round(hum, 2)
            return {
                "temperature": temp,
                "humidity": hum,
            }
        else:
            return "Invalid sensor readings."
    except OSError as e:
        return "Failed to read sensor."


def web_page(data):
    html = (
        """<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h2 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.2rem; }
    .dht-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
  </style>
</head>
<body>
  <h2>ESP DHT Server</h2>
  <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="dht-labels">Temperature</span> 
    <span>"""
        + str(data["temperature"])
        + """</span>
    <sup class="units">&deg;C</sup>
  </p>
  <p>
    <i class="fas fa-tint" style="color:#00add6;"></i> 
    <span class="dht-labels">Humidity</span>
    <span>"""
        + str(data["humidity"])
        + """</span>
    <sup class="units">%</sup>
  </p>
</body>
</html>"""
    )
    return html


def restart():
    print("Failed to connect to MQTT broker. Reconnecting...")
    time.sleep(10)
    machine.reset()


def setup_mqtt_client(config):
    mqtt_server = config["mqtt_server"]
    client_id = config["client_id"]
    print("%s %s" % (mqtt_server, client_id))
    client = MQTTClient(client_id, mqtt_server, port=1883, keepalive=60)
    try:
        client.connect()
        print("Connected to %s MQTT broker" % (mqtt_server))
        return client
    except OSError as e:
        restart()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 80))
s.listen(5)

client = setup_mqtt_client(config)

last_send = 0
while True:
    sensor_readings = read_sensor()

    if (time.time() - last_send) > int(config["message_interval_s"]):
        print("Sending message")
        client.publish(
            "home/living-room/temperature", str(sensor_readings["temperature"])
        )
        client.publish("home/living-room/humidity", str(sensor_readings["humidity"]))
        last_send = time.time()

    r, w, err = select((s,), (), (), 1)
    if r:
        for readable in r:
            conn, addr = s.accept()
            try:
                print("Got a connection from %s" % str(addr))
                request = conn.recv(1024)
                response = web_page(sensor_readings)
                conn.send("HTTP/1.1 200 OK\n")
                conn.send("Content-Type: text/html\n")
                conn.send("Connection: close\n\n")
                conn.sendall(response)
                conn.close()
            except OSError as e:
                pass
