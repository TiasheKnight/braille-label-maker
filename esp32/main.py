"""Main entry point for Braille Label Maker (MicroPython ESP32)"""

import time

# Initialize all components
from components import (
    wifi_manager, solenoids, roller_motor, vibration,
    audio, camera_module, power
)

from handlers import (
    print_handler, feed_handler, camera_handler,
    voice_to_braille, camera_to_braille, web_handler
)

from test_components import startup_tests


def main():
    """Main entry point"""
    
    # Wait a bit for the serial monitor to catch up
    time.sleep(1)
    
    print("\n" + "=" * 50)
    print("Braille Label Maker (MicroPython)")
    print("=" * 50 + "\n")
    
    # Initialize WiFi
    wifi_manager.init_wifi()
    
    # Initialize components
    solenoids.init()
    roller_motor.init()
    vibration.init()
    power.init()
    
    # Initialize handlers
    print_handler.init()
    feed_handler.init()
    camera_handler.init()
    voice_to_braille.init()
    camera_to_braille.init()
    web_handler.init()
    
    # Run startup tests
    startup_tests.run_all()
    
    # Start web server (this blocks)
    print("Starting web server...")
    web_handler.start_web_server(port=80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutdown requested")
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
