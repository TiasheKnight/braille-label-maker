#pragma once

#include <Arduino.h>
#include "../components/solenoids.h"
#include "../components/roller_motor.h"
#include "../components/servo.h"
#include "../handlers/servo_handler.h"

namespace StartupTests {
  inline bool testSolenoid() {
    Serial.print("[TEST] Solenoid (3 pulses)... ");
    Solenoids::init();
    Solenoids::stampThreeTimes(100, 180);
    Serial.println("OK");
    return true;
  }

  inline bool testFeedMotors() {
    Serial.print("[TEST] Feed motors forward/reverse... ");
    RollerMotor::init();
    RollerMotor::feedForward(128);
    delay(120);
    RollerMotor::feedReverse(128);
    RollerMotor::stop();
    Serial.println("OK");
    return true;
  }

  inline bool testServoTemplates() {
    Serial.print("[TEST] Servo template 7 positions... ");
    ServoHandler::init();
    ServoSelector::sweepAllPositions(220);
    ServoHandler::home();
    Serial.println("OK");
    return true;
  }

  inline void runAll() {
    Serial.println("Starting stripped-down startup tests...");
    bool result = true;

    result &= testFeedMotors();
    result &= testServoTemplates();
    result &= testSolenoid();

    if (result) {
      Serial.println("[TEST] ALL COMPONENTS OK");
    } else {
      Serial.println("[TEST] SOME COMPONENTS FAILED");
    }
  }
}
