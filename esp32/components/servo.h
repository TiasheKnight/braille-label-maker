#pragma once

#include <ESP32Servo.h>

namespace ServoControl {
  inline const int SERVO_PIN = 3;
  inline Servo servo;

  inline void init() {
    servo.attach(SERVO_PIN);
    servo.write(0);  // Start at 0 degrees
  }

  inline void setPosition(int position) {
    // 7 positions: 0 to 6, mapping to 0 to 180 degrees
    if (position < 0) position = 0;
    if (position > 6) position = 6;
    int angle = (position * 180) / 6;  // 0, 30, 60, 90, 120, 150, 180
    servo.write(angle);
  }

  inline void selectTemplate(int templateIndex) {
    setPosition(templateIndex);
  }
}
