#pragma once

#include <Arduino.h>
#include "../components/solenoids.h"
#include "../components/braille.h"
#include "feed_handler.h"
#include "servo_handler.h"

namespace PrintHandler {
  inline void init() {
    Solenoids::init();
    FeedHandler::init();
    ServoHandler::init();
  }

  inline void printColumn(const String& pattern) {
    if (!ServoHandler::selectPattern(pattern)) {
      return;
    }

    Solenoids::stampThreeTimes();
  }

  inline void printChar(const String& pattern) {
    const String leftColumn = pattern.substring(0, 3);
    const String rightColumn = pattern.substring(3, 6);

    printColumn(leftColumn);
    FeedHandler::advanceAfterColumn();

    printColumn(rightColumn);
    FeedHandler::advanceAfterCharacter();

    ServoHandler::home();
  }

  inline void printText(const String& text) {
    for (int i = 0; i < text.length(); i++) {
      String pattern = Braille::mapCharToPattern(tolower(text[i]));
      printChar(pattern);
    }
  }
}
