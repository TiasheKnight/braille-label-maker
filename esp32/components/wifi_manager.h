#pragma once

#include <WiFi.h>

namespace WifiManager {
  inline const char* SSID = "YourWiFiSSID";
  inline const char* PASSWORD = "YourWiFiPassword";

  inline void initWiFi() {
    WiFi.mode(WIFI_STA);
    WiFi.begin(SSID, PASSWORD);

    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }

    Serial.println("\nWiFi connected");
    Serial.print("IP Address: http://");
    Serial.println(WiFi.localIP());
  }

  inline bool connected() {
    return WiFi.status() == WL_CONNECTED;
  }
}
