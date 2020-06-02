import network
import time

WiFi_SSID = "Rely"
WiFi_PASS = "12345678"

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(WiFi_SSID,WiFi_PASS)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
