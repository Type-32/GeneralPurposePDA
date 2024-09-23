import time

import esp
import network

def main():
    print("ello")
    connect_wifi('SIA', '')

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            print('WiFi is not connected...', wlan.ifconfig())
            time.sleep(1)
    print('WiFi connected:', wlan.ifconfig())

if __name__ == '__main__':
    main()