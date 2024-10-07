import time
import network
import urequests


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

def search_internet(query: str) -> any:
    url = 'https://api.duckduckgo.com/?q=' + query + '&format=json&pretty=1&no_html=1'
    response = urequests.get(url)
    data = response.json()
    response.close()
    return data

def search_dnd(category: str, query: str) -> any:
    url = 'https://www.dnd5eapi.co/api/' + category + '/?name=' + query
    response = urequests.get(url)
    data = response.json()
    response.close()
    return data

def get_dnd(category: str, index: str) -> any:
    url = 'https://www.dnd5eapi.co/api/' + category + '/' + index
    response = urequests.get(url)
    data = response.json()
    response.close()
    return data

def is_wifi_connected():
    wlan = network.WLAN(network.STA_IF)
    return wlan.isconnected()

def disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(False)
    print('WiFi disconnected')