"""Camera to Braille handler for MicroPython ESP32"""

from handlers import camera_handler, print_handler


def init():
    """Initialize camera to Braille handler"""
    camera_handler.init()


def capture_and_print():
    """Capture image and print scanned text as Braille"""
    scanned = camera_handler.capture_and_analyze()
    if not scanned:
        print("CameraToBraille: no text captured")
        return
    
    print(f"Scanner text: {scanned}")
    print_handler.print_text(scanned)
