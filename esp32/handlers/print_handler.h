#pragma once

#include <Arduino.h>
#include "../components/solenoids.h"
#include "../components/braille.h"
#include "../components/vibration.h"

namespace PrintHandler {
  inline void init() {
    // printer-specific warmup can go here
  }

  inline void printChar(const String& pattern) {
    String first = pattern.substring(0, 3);
    String second = pattern.substring(3, 6);

    Solenoids::firePattern(first);
    delay(250);
    Solenoids::firePattern(second);
    delay(400);
  }

  inline void printText(const String& text) {
    Vibration::notifyPrintStart();
    for (int i = 0; i < text.length(); i++) {
      String pattern = Braille::mapCharToPattern(tolower(text[i]));
      printChar(pattern);
    }
    Vibration::notifyPrintEnd();
  }
}
