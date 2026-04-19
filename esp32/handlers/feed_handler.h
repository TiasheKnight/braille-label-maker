#pragma once

#include <Arduino.h>
#include "../components/roller_motor.h"

namespace FeedHandler {
  inline const int DEFAULT_CHARACTER_FEED_STEPS = 256;
  inline const int DEFAULT_RETRACT_STEPS = 128;

  inline void init() {
    RollerMotor::init();
  }

  inline void advanceLabel(int steps = DEFAULT_CHARACTER_FEED_STEPS) {
    RollerMotor::feedForward(steps);
  }

  inline void retractLabel(int steps = DEFAULT_RETRACT_STEPS) {
    RollerMotor::feedReverse(steps);
  }

  inline void advanceAfterColumn() {
    advanceLabel(DEFAULT_CHARACTER_FEED_STEPS / 2);
  }

  inline void advanceAfterCharacter() {
    advanceLabel(DEFAULT_CHARACTER_FEED_STEPS);
  }
}
