#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <secrets.h>

WebServer server(80);

#include "../handlers/web_handler.h"

void setup() {
  Serial.begin(115200);
  delay(300);
  Serial.println();
  Serial.println("Braille label maker — starting");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("WiFi connecting to ");
  Serial.println(WIFI_SSID);
  uint8_t tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 80) {
    delay(250);
    Serial.print(".");
    tries++;
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("WiFi connected. IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("WiFi connection failed — check secrets.h SSID/password.");
  }

  PrintHandler::init();
  WebHandler::init();
}

void loop() {
  server.handleClient();
}
