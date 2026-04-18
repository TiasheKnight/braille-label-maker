#pragma once

#include <Arduino.h>

namespace RollerMotor {
  inline const int FEED_MOTOR_1_PINS[] = {9, 10, 11, 12};
  inline const int FEED_MOTOR_2_PINS[] = {4, 5, 6, 7};
  inline const int STEPS_PER_REV = 2048;
  inline const int DEFAULT_STEP_DELAY_MS = 2;
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
      pinMode(FEED_MOTOR_1_PINS[i], OUTPUT);
      pinMode(FEED_MOTOR_2_PINS[i], OUTPUT);
      digitalWrite(FEED_MOTOR_1_PINS[i], LOW);
      digitalWrite(FEED_MOTOR_2_PINS[i], LOW);
    }
  }

  inline void applyStep(const int pins[], int stepIndex) {
    for (int i = 0; i < 4; i++) {
      digitalWrite(pins[i], STEP_SEQUENCE[stepIndex][i]);
    }
  }

  inline void releaseMotor(const int pins[]) {
    for (int i = 0; i < 4; i++) {
      digitalWrite(pins[i], LOW);
    }
  }

  inline void stop() {
    releaseMotor(FEED_MOTOR_1_PINS);
    releaseMotor(FEED_MOTOR_2_PINS);
  }

  inline void feedSteps(int steps, bool forward = true, int stepDelayMs = DEFAULT_STEP_DELAY_MS) {
    const int direction = forward ? 1 : -1;
    int phase = 0;

    for (int i = 0; i < steps; i++) {
      phase = (phase + direction + 8) % 8;
      applyStep(FEED_MOTOR_1_PINS, phase);
      applyStep(FEED_MOTOR_2_PINS, phase);
      delay(stepDelayMs);
    }

    stop();
  }

  inline void feedForward(int steps = 512, int stepDelayMs = DEFAULT_STEP_DELAY_MS) {
    feedSteps(steps, true, stepDelayMs);
  }

  inline void feedReverse(int steps = 512, int stepDelayMs = DEFAULT_STEP_DELAY_MS) {
    feedSteps(steps, false, stepDelayMs);
  }
}
