from umqtt.simple import MQTTClient
from machine import Pin
from dht import DHT11
import network
import time
import json

d = DHT11(Pin(4, Pin.IN))
SERVER = "broker.mqtt-dashboard.com"
TOPIC = b"esp32/te/python"
client = MQTTClient("umqtt_client", SERVER)
client.connect()

while True:
  d.measure()
  t=d.temperature()
  h=d.humidity()
  payload = {"temp":t,"humid":h}
  print('Temperature=', t, 'C', 'humid', h, '%')

  client.publish(TOPIC,json.dumps(payload))
  time.sleep(5)
