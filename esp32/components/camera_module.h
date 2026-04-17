#pragma once

#include <Arduino.h>

namespace CameraModule {
  inline void init() {
    Serial.println("Camera: init placeholder");
    // TODO: initialize the ESP32-S3 camera module and PSRAM if available.
  }

  inline bool captureFrame() {
    Serial.println("Camera: captureFrame placeholder");
    // TODO: return true when a frame is successfully captured.
    return true;
  }

  inline String scanText() {
    Serial.println("Camera: scanText placeholder");
    // TODO: perform OCR or image analysis and return recognized text.
    return String();
  }
}
