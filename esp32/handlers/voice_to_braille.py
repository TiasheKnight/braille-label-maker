"""Voice to Braille handler for MicroPython ESP32"""

from components import audio
from handlers import print_handler


def init():
    """Initialize voice handler"""
    audio.init()


def listen_and_print():
    """Listen for voice command and print as Braille"""
    command = audio.listen_command()
    if not command:
        print("Voice: no command detected")
        return
    
    print(f"Voice command: {command}")
    print_handler.print_text(command)
