"""Vibration motor control for MicroPython ESP32"""

import machine
import time

VIB_PIN = 15
vib_pin = None


def init():
    """Initialize vibration motor pin"""
    global vib_pin
    vib_pin = machine.Pin(VIB_PIN, machine.Pin.OUT)
    vib_pin.off()


def pulse(duration_ms=80):
    """Vibrate for specified duration"""
    vib_pin.on()
    time.sleep_ms(duration_ms)
    vib_pin.off()


def notify_command_received():
    """Double pulse to notify command received"""
    pulse(50)
    time.sleep_ms(100)
    pulse(50)


def notify_print_start():
    """Single pulse to notify print start"""
    pulse(200)


def notify_print_end():
    """Double pulse to notify print end"""
    pulse(100)
    time.sleep_ms(100)
    pulse(100)
