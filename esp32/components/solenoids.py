"""Solenoid control for MicroPython ESP32"""

import machine
import time

PINS = [18, 19, 21]  # 3 solenoids
gpio_pins = []


def init():
    """Initialize solenoid GPIO pins"""
    global gpio_pins
    gpio_pins = [machine.Pin(pin, machine.Pin.OUT) for pin in PINS]
    for pin in gpio_pins:
        pin.off()


def pulse(index, duration_ms=120):
    """Pulse a single solenoid"""
    if index < 0 or index >= len(gpio_pins):
        return
    
    gpio_pins[index].on()
    time.sleep_ms(duration_ms)
    gpio_pins[index].off()


def fire_pattern(pattern):
    """Fire solenoids based on a binary pattern string"""
    for i, char in enumerate(pattern):
        if i < len(gpio_pins) and char == '1':
            pulse(i)
