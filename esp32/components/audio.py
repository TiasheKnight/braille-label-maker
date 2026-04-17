"""Audio component placeholder for MicroPython ESP32"""

import machine

I2S_WS_PIN = 0  # Placeholder
I2S_SCK_PIN = 1  # Placeholder
I2S_SD_PIN = 2  # Placeholder


def init():
    """Initialize audio/microphone"""
    print("Audio: init placeholder")
    # TODO: initialize I2S microphone pins and DMA buffer


def listen_command():
    """Listen and return voice command"""
    print("Audio: listen_command placeholder")
    # TODO: implement voice capture and speech-to-text
    return ""
