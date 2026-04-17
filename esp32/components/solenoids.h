#pragma once

#include <Arduino.h>

namespace Solenoids {
  inline const int PINS[] = {18, 19, 21};
  inline const int COUNT = sizeof(PINS) / sizeof(PINS[0]);

  inline void init() {
    for (int i = 0; i < COUNT; i++) {
      pinMode(PINS[i], OUTPUT);
      digitalWrite(PINS[i], LOW);
    }
  }

  inline void pulse(int index, int durationMs = 120) {
    if (index < 0 || index >= COUNT) {
      return;
    }
    digitalWrite(PINS[index], HIGH);
    delay(durationMs);
    digitalWrite(PINS[index], LOW);
  }

  inline void firePattern(const String& pattern) {
    for (int i = 0; i < COUNT && i < pattern.length(); i++) {
      if (pattern[i] == '1') {
        pulse(i);
      }
    }
  }
}
