#pragma once

#include <Arduino.h>

namespace RollerMotor {
  inline const int PWM_PIN = 22;
  inline const int DIR_PIN = 23;
  inline const int MOTOR_CHANNEL = 0;
  inline const int MOTOR_FREQUENCY = 2000;
  inline const int MOTOR_RESOLUTION = 8;

  inline void init() {
    pinMode(DIR_PIN, OUTPUT);
    ledcSetup(MOTOR_CHANNEL, MOTOR_FREQUENCY, MOTOR_RESOLUTION);
    ledcAttachPin(PWM_PIN, MOTOR_CHANNEL);
    ledcWrite(MOTOR_CHANNEL, 0);
  }

  inline void setSpeed(uint8_t speed) {
    ledcWrite(MOTOR_CHANNEL, speed);
  }

  inline void feedForward(uint8_t speed = 180) {
    digitalWrite(DIR_PIN, HIGH);
    ledcWrite(MOTOR_CHANNEL, speed);
  }

  inline void feedReverse(uint8_t speed = 180) {
    digitalWrite(DIR_PIN, LOW);
    ledcWrite(MOTOR_CHANNEL, speed);
  }

  inline void stop() {
    ledcWrite(MOTOR_CHANNEL, 0);
  }
}
