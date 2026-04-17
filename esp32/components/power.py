"""Power management for MicroPython ESP32"""

import machine
import esp32

BATTERY_PIN = 35  # ADC pin for battery voltage
VOLTAGE_DIVIDER_RATIO = 2.0
ADC_REFERENCE = 3.3
ADC_MAX = 4095

adc = None


def init():
    """Initialize power monitoring"""
    global adc
    adc = machine.ADC(machine.Pin(BATTERY_PIN))
    adc.atten(machine.ADC.ATTN_11DB)  # Full range 0-3.6V


def read_battery_voltage():
    """Read battery voltage from ADC"""
    if not adc:
        return 0.0
    
    raw = adc.read()
    voltage = (raw / ADC_MAX) * ADC_REFERENCE * VOLTAGE_DIVIDER_RATIO
    return voltage


def is_battery_healthy(min_voltage=3.3):
    """Check if battery voltage is healthy"""
    return read_battery_voltage() >= min_voltage
