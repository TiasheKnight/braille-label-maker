#pragma once

#include <Arduino.h>

namespace Power {
  inline const int BATTERY_PIN = A0;
  inline const float VOLTAGE_DIVIDER_RATIO = 2.0f;
  inline const float ADC_REFERENCE = 3.3f;
  inline const int ADC_MAX = 4095;

  inline void init() {
    pinMode(BATTERY_PIN, INPUT);
  }

  inline float readBatteryVoltage() {
    int raw = analogRead(BATTERY_PIN);
    float voltage = (raw / float(ADC_MAX)) * ADC_REFERENCE * VOLTAGE_DIVIDER_RATIO;
    return voltage;
  }

  inline bool isBatteryHealthy(float minVoltage = 3.3f) {
    return readBatteryVoltage() >= minVoltage;
  }
}
