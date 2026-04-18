#pragma once

#include <Arduino.h>
#include "../components/servo.h"

namespace ServoHandler {
  inline int patternToTemplatePosition(const String& pattern) {
    if (pattern.length() != 3 || pattern == "000") {
      return -1;
    }

    int value = 0;
    for (int i = 0; i < 3; i++) {
      value <<= 1;
      value |= (pattern[i] == '1') ? 1 : 0;
    }

    return constrain(value - 1, 0, ServoSelector::POSITION_COUNT - 1);
  }

  inline void init() {
    ServoSelector::init();
  }

  inline bool selectPattern(const String& pattern) {
    const int position = patternToTemplatePosition(pattern);
    if (position < 0) {
      return false;
    }

    ServoSelector::moveToPosition(position);
    return true;
  }

  inline void home() {
    ServoSelector::moveToPosition(0);
  }
}
