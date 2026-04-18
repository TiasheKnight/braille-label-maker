#pragma once

#include <Arduino.h>
#include "../components/solenoids.h"
#include "../components/braille.h"

namespace PrintHandler {
  inline void init() {
    // printer-specific warmup can go here
  }

  inline void printChar(const String& pattern) {
    // For each '1' in the pattern, fire the solenoid three times
    for (int i = 0; i < pattern.length(); i++) {
      if (pattern[i] == '1') {
        Solenoids::fireThreeTimes();
        delay(500);  // Delay between dots
      }
    }
  }

  inline void printText(const String& text) {
    for (int i = 0; i < text.length(); i++) {
      String pattern = Braille::mapCharToPattern(tolower(text[i]));
      printChar(pattern);
      delay(1000);  // Delay between characters
    }
  }
}
