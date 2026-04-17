import serial
import time
from braille_logic import text_to_braille

# Change COM port if needed
ser = serial.Serial('COM5', 115200, timeout=1)
time.sleep(2)


def send_text(text):
    braille = text_to_braille(text)

    for char in braille:
        ser.write((char + "\n").encode())
        print("Sent:", char)
        time.sleep(0.4)


if __name__ == "__main__":
    while True:
        text = input("Enter label: ")
        send_text(text)
