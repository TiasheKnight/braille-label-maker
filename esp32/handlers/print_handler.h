#pragma once

#include <Arduino.h>
#include <ArduinoJson.h>
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

  /** Each cell: [[d1,d2,d3],[d4,d5,d6]] matching backend `encode_to_braille` cells. */
  inline void printBrailleCells(JsonArray cells) {
    for (JsonVariant cellVar : cells) {
      JsonArray cell = cellVar.as<JsonArray>();
      if (cell.size() < 2) continue;
      JsonArray left = cell[0].as<JsonArray>();
      JsonArray right = cell[1].as<JsonArray>();
      String pattern = "";
      for (unsigned i = 0; i < 3 && i < left.size(); i++) {
        pattern += (int)left[i] ? "1" : "0";
      }
      while (pattern.length() < 3) pattern += "0";
      for (unsigned i = 0; i < 3 && i < right.size(); i++) {
        pattern += (int)right[i] ? "1" : "0";
      }
      while (pattern.length() < 6) pattern += "0";
      printChar(pattern);
    }
  }
}
