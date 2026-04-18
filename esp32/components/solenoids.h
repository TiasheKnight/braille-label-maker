#pragma once

#include <Arduino.h>

namespace Solenoids {
  inline const int MOSFET_PIN = 8;  // Gate pin for IRFZ44N MOSFET

  inline void init() {
    pinMode(MOSFET_PIN, OUTPUT);
    digitalWrite(MOSFET_PIN, LOW);
  }

  inline void pulse(int durationMs = 120) {
    digitalWrite(MOSFET_PIN, HIGH);
    delay(durationMs);
    digitalWrite(MOSFET_PIN, LOW);
  }

  inline void fireThreeTimes() {
    for (int i = 0; i < 3; i++) {
      pulse();
      delay(200);  // Delay between pulses
    }
  }
}
