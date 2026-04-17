"""Camera handler for MicroPython ESP32-S3"""

from components import camera_module


def init():
    """Initialize camera"""
    camera_module.init()


def capture_and_analyze():
    """Capture frame and analyze text"""
    if not camera_module.capture_frame():
        return ""
    return camera_module.scan_text()
