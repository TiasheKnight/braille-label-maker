"""Startup tests for MicroPython ESP32"""

from components import (
    wifi_manager, solenoids, roller_motor, vibration,
    audio, camera_module, power
)


def test_wifi():
    """Test WiFi connectivity"""
    print("[TEST] WiFi... ", end="")
    if not wifi_manager.connected():
        print("FAIL (not connected)")
        return False
    print("OK")
    return True


def test_solenoids():
    """Test solenoid pulses"""
    print("[TEST] Solenoids... ", end="")
    solenoids.init()
    solenoids.pulse(0, 40)
    solenoids.pulse(1, 40)
    solenoids.pulse(2, 40)
    print("OK")
    return True


def test_roller_motor():
    """Test roller motor"""
    print("[TEST] Roller motor... ", end="")
    roller_motor.init()
    roller_motor.feed_forward(100)
    import time
    time.sleep_ms(100)
    roller_motor.stop()
    print("OK")
    return True


def test_vibration():
    """Test vibration motor"""
    print("[TEST] Vibration... ", end="")
    vibration.init()
    vibration.pulse(40)
    print("OK")
    return True


def test_audio():
    """Test audio initialization"""
    print("[TEST] Audio... ", end="")
    audio.init()
    print("OK (placeholder)")
    return True


def test_camera():
    """Test camera initialization"""
    print("[TEST] Camera... ", end="")
    camera_module.init()
    camera_module.capture_frame()
    print("OK (placeholder)")
    return True


def test_power():
    """Test power monitoring"""
    print("[TEST] Power... ", end="")
    power.init()
    voltage = power.read_battery_voltage()
    print(f"{voltage:.2f}V")
    return True


def run_all():
    """Run all startup tests"""
    print("\nStarting component startup tests...\n")
    
    result = True
    result &= test_wifi()
    result &= test_solenoids()
    result &= test_roller_motor()
    result &= test_vibration()
    result &= test_audio()
    result &= test_camera()
    result &= test_power()
    
    print()
    if result:
        print("[TEST] ALL COMPONENTS OK\n")
    else:
        print("[TEST] SOME COMPONENTS FAILED\n")
    
    return result
