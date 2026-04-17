#pragma once

#include <Arduino.h>
#include "../components/wifi_manager.h"
#include "../components/solenoids.h"
#include "../components/roller_motor.h"
#include "../components/vibration.h"
#include "../components/audio.h"
#include "../components/camera_module.h"
#include "../components/power.h"

namespace StartupTests {
  inline bool testWiFi() {
    Serial.print("[TEST] WiFi... ");
    if (!WifiManager::connected()) {
      Serial.println("FAIL (not connected)");
      return false;
    }
    Serial.println("OK");
    return true;
  }

  inline bool testSolenoids() {
    Serial.print("[TEST] Solenoids... ");
    Solenoids::init();
    Solenoids::pulse(0, 40);
    Solenoids::pulse(1, 40);
    Solenoids::pulse(2, 40);
    Serial.println("OK");
    return true;
  }

  inline bool testRollerMotor() {
    Serial.print("[TEST] Roller motor... ");
    RollerMotor::init();
    RollerMotor::feedForward(100);
    delay(100);
    RollerMotor::stop();
    Serial.println("OK");
    return true;
  }

  inline bool testVibration() {
    Serial.print("[TEST] Vibration... ");
    Vibration::init();
    Vibration::pulse(40);
    Serial.println("OK");
    return true;
  }

  inline bool testAudio() {
    Serial.print("[TEST] Audio... ");
    Audio::init();
    Serial.println("OK (placeholder)");
    return true;
  }

  inline bool testCamera() {
    Serial.print("[TEST] Camera... ");
    CameraModule::init();
    CameraModule::captureFrame();
    Serial.println("OK (placeholder)");
    return true;
  }

  inline bool testPower() {
    Serial.print("[TEST] Power... ");
    Power::init();
    float voltage = Power::readBatteryVoltage();
    Serial.print(voltage, 2);
    Serial.println(" V");
    return true;
  }

  inline void runAll() {
    Serial.println("Starting component startup tests...");
    bool result = true;

    result &= testWiFi();
    result &= testSolenoids();
    result &= testRollerMotor();
    result &= testVibration();
    result &= testAudio();
    result &= testCamera();
    result &= testPower();

    if (result) {
      Serial.println("[TEST] ALL COMPONENTS OK");
    } else {
      Serial.println("[TEST] SOME COMPONENTS FAILED");
    }
  }
}
