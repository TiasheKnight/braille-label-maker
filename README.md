# Braille Label Maker

A standalone ESP32-based Braille demo that uses 3 solenoids and a web UI for input.

## Repository Structure

```
./
│── python_dev/
│   ├── braille_logic.py
│   ├── sender.py
│
│── esp32/
│   ├── platformio.ini
│   └── src/main.cpp
```

## Recommended architecture

```
[ Phone / Laptop Browser ]
            ↓ Same WiFi Network
        ESP32 Web Server
            ↓
     Braille Logic (C++)
            ↓
      3 Solenoids (GPIO)
```

### Why this is better

- Fully embedded: the ESP32 hosts the UI and prints Braille without a laptop.
- Easy demo: connect your phone to the same WiFi as the ESP32.
- Still includes serial fallback for debugging or Python-driven demo mode.

## ESP32 side

### `esp32/platformio.ini`

- Configures PlatformIO for an ESP32 Arduino build.
- Uses `monitor_speed = 115200`.

### `esp32/src/main.cpp`

- Connects to your existing WiFi network.
- Serves a simple web page at `/` with a text input.
- Handles `/print?text=...` to trigger Braille printing.
- Keeps serial fallback enabled for direct input.

## How to use the device

1. Flash the project in `esp32/` using PlatformIO.
2. Update the WiFi credentials in `esp32/src/main.cpp`:

   ```cpp
   const char* ssid = "YourWiFiSSID";
   const char* password = "YourWiFiPassword";
   ```

3. Power the ESP32.
4. Check the serial monitor for the IP address (e.g., `http://192.168.1.100`).
5. Connect your phone or laptop to the same WiFi network.
6. Open the IP address in a browser.
7. Type text and tap `Print`.

## Hardware notes

- Use 3 solenoids or actuators connected to the ESP32 output pins.
- Default pins are `18`, `19`, and `21`.
- The ESP32 sends two 3-dot passes per character.

## Python integration (optional)

Python is now optional and can be used for testing or serial demo mode.

### `python_dev/braille_logic.py`

- Contains a 6-dot Braille map for letters `a` through `z` and space.
- Converts input text into a list of 6-character binary strings.

### `python_dev/sender.py`

- Opens a serial connection to the ESP32.
- Sends text directly over serial as a newline-terminated command.

#### Run it

1. Install `pyserial` if needed:

```bash
pip install pyserial
```

2. Update the COM port in `python_dev/sender.py` if necessary.
3. Run:

```bash
python python_dev/sender.py
```

4. Type a label and press Enter.

## Testing without hardware

In `python_dev/braille_logic.py`, you can test conversion manually:

```python
from braille_logic import text_to_braille
print(text_to_braille("hello"))
```

Expected output:

```text
['110010', '100010', '111000', '111000', '101010']
```
