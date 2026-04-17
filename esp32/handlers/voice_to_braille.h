#pragma once

#include <Arduino.h>
#include "../components/audio.h"
#include "../components/braille.h"
#include "print_handler.h"

namespace VoiceToBraille {
  inline void init() {
    Audio::init();
  }

  inline void listenAndPrint() {
    String command = Audio::listenCommand();
    if (command.length() == 0) {
      Serial.println("Voice: no command detected");
      return;
    }

    Serial.print("Voice command: ");
    Serial.println(command);
    PrintHandler::printText(command);
  }
}
