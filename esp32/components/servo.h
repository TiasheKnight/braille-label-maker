#pragma once

#include <Arduino.h>

namespace ServoSelector {
  inline const int SERVO_PIN = 3;
  inline const int POSITION_COUNT = 7;
  inline const int MIN_ANGLE = 0;
  inline const int MAX_ANGLE = 180;
  inline const int SERVO_SETTLE_MS = 350;
  inline const int PULSE_MIN_US = 500;
  inline const int PULSE_MAX_US = 2400;

  inline int currentPosition = 0;

  inline int positionToAngle(int position) {
    position = constrain(position, 0, POSITION_COUNT - 1);
    if (POSITION_COUNT <= 1) {
      return MIN_ANGLE;
    }

    return MIN_ANGLE + ((MAX_ANGLE - MIN_ANGLE) * position) / (POSITION_COUNT - 1);
  }

  inline void writePulseMicros(int pulseWidthUs) {
    digitalWrite(SERVO_PIN, HIGH);
    delayMicroseconds(pulseWidthUs);
    digitalWrite(SERVO_PIN, LOW);
  }

  inline void holdAngle(int angle, uint32_t holdMs = SERVO_SETTLE_MS) {
    angle = constrain(angle, MIN_ANGLE, MAX_ANGLE);
    const int pulseWidthUs = map(angle, 0, 180, PULSE_MIN_US, PULSE_MAX_US);
    const uint32_t pulseCount = max<uint32_t>(1, holdMs / 20);

    for (uint32_t i = 0; i < pulseCount; i++) {
      writePulseMicros(pulseWidthUs);
      delay(20);
    }
  }

  inline void init() {
    pinMode(SERVO_PIN, OUTPUT);
    digitalWrite(SERVO_PIN, LOW);
    holdAngle(positionToAngle(currentPosition), 500);
  }

  inline void moveToPosition(int position, uint32_t settleMs = SERVO_SETTLE_MS) {
    currentPosition = constrain(position, 0, POSITION_COUNT - 1);
    holdAngle(positionToAngle(currentPosition), settleMs);
  }

  inline void sweepAllPositions(uint32_t settleMs = 250) {
    for (int position = 0; position < POSITION_COUNT; position++) {
      moveToPosition(position, settleMs);
    }
    moveToPosition(0, settleMs);
  }
}
