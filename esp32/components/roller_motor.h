#pragma once

#include <Arduino.h>

namespace RollerMotor {
  // Stepper 1: GPIO 9,10,11,12
  inline const int STEPPER1_PINS[4] = {9, 10, 11, 12};
  // Stepper 2: GPIO 4,5,6,7
  inline const int STEPPER2_PINS[4] = {4, 5, 6, 7};

  // Half-step sequence for 28BYJ-48
  inline const int STEPS_PER_REV = 4096;  // 28BYJ-48 has 4096 steps per revolution
  inline const int STEP_SEQUENCE[8][4] = {
    {1, 0, 0, 0},
    {1, 1, 0, 0},
    {0, 1, 0, 0},
    {0, 1, 1, 0},
    {0, 0, 1, 0},
    {0, 0, 1, 1},
    {0, 0, 0, 1},
    {1, 0, 0, 1}
  };

  inline void init() {
    for (int i = 0; i < 4; i++) {
      pinMode(STEPPER1_PINS[i], OUTPUT);
      pinMode(STEPPER2_PINS[i], OUTPUT);
      digitalWrite(STEPPER1_PINS[i], LOW);
      digitalWrite(STEPPER2_PINS[i], LOW);
    }
  }

  inline void stepMotor(const int pins[4], int step, bool direction) {
    int seqIndex = direction ? step % 8 : (7 - step % 8);
    for (int i = 0; i < 4; i++) {
      digitalWrite(pins[i], STEP_SEQUENCE[seqIndex][i]);
    }
  }

  inline void rotateMotor(const int pins[4], int steps, bool direction, int delayMs = 2) {
    for (int i = 0; i < steps; i++) {
      stepMotor(pins, i, direction);
      delay(delayMs);
    }
    // Turn off coils
    for (int i = 0; i < 4; i++) {
      digitalWrite(pins[i], LOW);
    }
  }

  inline void feedForward(int steps = 100, int delayMs = 2) {
    rotateMotor(STEPPER1_PINS, steps, true, delayMs);
  }

  inline void feedReverse(int steps = 100, int delayMs = 2) {
    rotateMotor(STEPPER1_PINS, steps, false, delayMs);
  }

  inline void selectTemplate(int position) {
    // Assuming 7 positions, each ~25.7 degrees (180/7)
    int steps = (position * STEPS_PER_REV) / 7;
    rotateMotor(STEPPER2_PINS, steps, true);
  }
}
