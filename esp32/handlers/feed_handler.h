#pragma once

#include <Arduino.h>
#include "../components/roller_motor.h"

namespace FeedHandler {
  inline void init() {
    RollerMotor::init();
  }

  inline void advanceLabel(int steps = 100) {
    RollerMotor::feedForward(steps);
  }

  inline void retractLabel(int steps = 100) {
    RollerMotor::feedReverse(steps);
  }
}
