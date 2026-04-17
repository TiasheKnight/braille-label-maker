"""Print handler for MicroPython ESP32"""

from components import solenoids, braille, vibration


def init():
    """Initialize printer"""
    pass


def print_char(pattern):
    """Print a single character (6-bit pattern)"""
    first = pattern[:3]
    second = pattern[3:6]
    
    solenoids.fire_pattern(first)
    import time
    time.sleep_ms(250)
    solenoids.fire_pattern(second)
    time.sleep_ms(400)


def print_text(text):
    """Print text as Braille"""
    vibration.notify_print_start()
    
    patterns = braille.text_to_braille(text)
    for pattern in patterns:
        print_char(pattern)
    
    vibration.notify_print_end()
