"""WiFi Manager for MicroPython ESP32"""

import network
import time

SSID = "YourWiFiSSID"
PASSWORD = "YourWiFiPassword"

wlan = None


def init_wifi():
    """Initialize WiFi connection"""
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"Connecting to WiFi {SSID}...")
        wlan.connect(SSID, PASSWORD)
        
        timeout = 0
        while not wlan.isconnected() and timeout < 20:
            time.sleep(0.5)
            print(".", end="")
            timeout += 1
        
        print()
    
    if wlan.isconnected():
        print("WiFi connected!")
        print(f"IP Address: http://{wlan.ifconfig()[0]}")
    else:
        print("WiFi connection failed!")


def connected():
    """Check if WiFi is connected"""
    return wlan is not None and wlan.isconnected()
