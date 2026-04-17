#pragma once

#include <Arduino.h>
#include "camera_handler.h"
#include "print_handler.h"

namespace CameraToBraille {
  inline void init() {
    CameraHandler::init();
  }

  inline void captureAndPrint() {
    String scanned = CameraHandler::captureAndAnalyze();
    if (scanned.length() == 0) {
      Serial.println("CameraToBraille: no text captured");
      return;
    }
    Serial.print("Scanner text: ");
    Serial.println(scanned);
    PrintHandler::printText(scanned);
  }
}
