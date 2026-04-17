#pragma once

#include <Arduino.h>

namespace Audio {
  inline const int I2S_WS_PIN = 0;   // placeholder
  inline const int I2S_SCK_PIN = 1;  // placeholder
  inline const int I2S_SD_PIN = 2;   // placeholder

  inline void init() {
    Serial.println("Audio: init placeholder");
    // TODO: initialize I2S microphone pins and DMA buffer.
  }

  inline String listenCommand() {
    // TODO: implement voice capture and speech-to-text.
    return String();
  }
}
