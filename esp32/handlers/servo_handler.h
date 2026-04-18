#pragma once

#include <Arduino.h>
#include "../components/servo.h"

namespace ServoHandler {
  inline void init() {
    ServoControl::init();
  }

  inline void selectTemplate(int templateIndex) {
    ServoControl::selectTemplate(templateIndex);
  }
}
