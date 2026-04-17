#pragma once

#include <Arduino.h>

namespace Vibration {
  inline const int VIB_PIN = 15;

  inline void init() {
    pinMode(VIB_PIN, OUTPUT);
    digitalWrite(VIB_PIN, LOW);
  }

  inline void pulse(int durationMs = 80) {
    digitalWrite(VIB_PIN, HIGH);
    delay(durationMs);
    digitalWrite(VIB_PIN, LOW);
  }

  inline void notifyCommandReceived() {
    pulse(50);
    delay(100);
    pulse(50);
  }

  inline void notifyPrintStart() {
    pulse(200);
  }

  inline void notifyPrintEnd() {
    pulse(100);
    delay(100);
    pulse(100);
  }
}
