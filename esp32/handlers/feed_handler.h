#pragma once

#include <Arduino.h>
#include "../components/roller_motor.h"

namespace FeedHandler {
  inline void init() {
    RollerMotor::init();
  }

  inline void advanceLabel(uint32_t durationMs = 800) {
    RollerMotor::feedForward(220);
    delay(durationMs);
    RollerMotor::stop();
  }

  inline void retractLabel(uint32_t durationMs = 500) {
    RollerMotor::feedReverse(220);
    delay(durationMs);
    RollerMotor::stop();
  }
}
