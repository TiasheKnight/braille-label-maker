#pragma once

#include <Arduino.h>

namespace Solenoids {
  inline const int MOSFET_PIN = 8;
  inline const int DEFAULT_PULSE_MS = 120;
  inline const int DEFAULT_GAP_MS = 200;

  inline void init() {
    pinMode(MOSFET_PIN, OUTPUT);
    digitalWrite(MOSFET_PIN, LOW);
  }

  inline void pulse(int durationMs = DEFAULT_PULSE_MS) {
    digitalWrite(MOSFET_PIN, HIGH);
    delay(durationMs);
    digitalWrite(MOSFET_PIN, LOW);
  }

  inline void stampThreeTimes(int pulseMs = DEFAULT_PULSE_MS, int gapMs = DEFAULT_GAP_MS) {
    for (int i = 0; i < 3; i++) {
      pulse(pulseMs);
      if (i < 2) {
        delay(gapMs);
      }
    }
  }
}
