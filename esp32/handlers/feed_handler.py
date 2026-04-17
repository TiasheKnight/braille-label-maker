"""Feed handler for MicroPython ESP32"""

from components import roller_motor
import time


def init():
    """Initialize feeder"""
    roller_motor.init()


def advance_label(duration_ms=800):
    """Advance label forward"""
    roller_motor.feed_forward(220)
    time.sleep_ms(duration_ms)
    roller_motor.stop()


def retract_label(duration_ms=500):
    """Retract label backward"""
    roller_motor.feed_reverse(220)
    time.sleep_ms(duration_ms)
    roller_motor.stop()
