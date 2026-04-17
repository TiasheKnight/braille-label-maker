#pragma once

#include <Arduino.h>
#include "../components/camera_module.h"

namespace CameraHandler {
  inline void init() {
    CameraModule::init();
  }

  inline String captureAndAnalyze() {
    if (!CameraModule::captureFrame()) {
      return String();
    }
    return CameraModule::scanText();
  }
}
