from machine import Pin
from time import sleep
import dht
from umqtt.simple import MQTTClient
import network
import secrets_kw

# Wi-Fi credentials
WIFI_SSID = secrets_kw.WIFI_SSID
WIFI_PASSWORD = secrets_kw.WIFI_PASSWORD

# Adafruit IO credentials
ADAFRUIT_IO_USERNAME = secrets_kw.ADAFRUIT_IO_USERNAME
ADAFRUIT_IO_KEY = secrets_kw.ADAFRUIT_IO_KEY

# Adafruit IO MQTT configuration
mqtt_server = 'io.adafruit.com'
client_id = 'your-device-id'
temperature_c_topic = '{}/feeds/dht_temperature_c'.format(ADAFRUIT_IO_USERNAME)
temperature_f_topic = '{}/feeds/dht_temperature_f'.format(ADAFRUIT_IO_USERNAME)
humidity_topic = '{}/feeds/dht_humidity'.format(ADAFRUIT_IO_USERNAME)

sensor = dht.DHT11(Pin(5))

# Function to connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print('Connected to Wi-Fi')

# Function to connect to Adafruit IO
def connect_to_mqtt():
    client = MQTTClient(client_id, mqtt_server, 0, ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.connect()
    return client

# Connect to Wi-Fi
connect_to_wifi()

while True:
    try:

        sensor.measure()
        t_celsius = sensor.temperature()
        t_fahrenheit = (t_celsius * 9/5) + 32
        h = sensor.humidity()

        # Connect to Adafruit IO
        client = connect_to_mqtt()

        # Publish to the respective feeds
        client.publish(temperature_c_topic, str(t_celsius))
        sleep(1)
        client.publish(temperature_f_topic, str(t_fahrenheit))
        sleep(1)
        client.publish(humidity_topic, str(h))

        # Disconnect from Adafruit IO
        client.disconnect()

        print('Temperature: %3.1f C' % t_celsius)
        print('Temperature: %3.1f F' % t_fahrenheit)
        print('Humidity: %3.1f %%' % h)
        sleep(10)
    except OSError as e:
        print('Sensor Reading Failed')
