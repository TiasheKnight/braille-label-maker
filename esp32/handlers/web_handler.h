#pragma once

#include <WebServer.h>
#include <WiFi.h>
#include <Arduino.h>
#include <ArduinoJson.h>
#include <string.h>
#include <secrets.h>

extern WebServer server;

#include "../components/braille.h"
#include "print_handler.h"

namespace WebHandler {

  inline void handleRoot() {
    String html = R"rawliteral(
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="utf-8"/>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Braille Label Maker</title>
          <style>body{font-family:system-ui,sans-serif;margin:24px;line-height:1.5;}</style>
        </head>
        <body>
          <h2>Braille Label Maker</h2>
          <p>Device is online. Confirmed prints are sent from the Flask backend via
          <code>POST /print-job</code> (form field <code>payload</code> = JSON with <code>print_code</code> + <code>cells</code>).</p>
          <p>IP: )rawliteral";
    html += WiFi.localIP().toString();
    html += R"rawliteral(</p>
        </body>
      </html>
    )rawliteral";
    server.send(200, "text/html", html);
  }

  /** Legacy GET print: requires <code>code</code> matching BRAILLE_PRINT_SECRET. */
  inline void handlePrint() {
    if (!server.hasArg("text")) {
      server.send(400, "text/plain", "Missing text");
      return;
    }
    if (!server.hasArg("code") || server.arg("code") != String(BRAILLE_PRINT_SECRET)) {
      Serial.println("[GET /print] rejected: missing or invalid code");
      server.send(403, "text/plain", "Forbidden");
      return;
    }
    String text = server.arg("text");
    PrintHandler::printText(text);
    String response = "<html><body><p>Printed: " + text + "</p><p><a href=\"/\">Back</a></p></body></html>";
    server.send(200, "text/html", response);
  }

  /**
   * Two-part job: JSON in form field `payload` with print_code (part 1) and cells (part 2).
   * Printing runs only after print_code matches BRAILLE_PRINT_SECRET.
   */
  inline void handlePrintJob() {
    if (!server.hasArg("payload")) {
      server.send(400, "text/plain", "missing payload");
      return;
    }

    String raw = server.arg("payload");
    JsonDocument doc(16384);
    DeserializationError err = deserializeJson(doc, raw);
    if (err) {
      Serial.printf("[POST /print-job] JSON error: %s\n", err.c_str());
      server.send(400, "text/plain", "invalid json");
      return;
    }

    const char* code = doc["print_code"] | "";
    if (strcmp(code, BRAILLE_PRINT_SECRET) != 0) {
      Serial.println("[POST /print-job] rejected: invalid print_code");
      server.send(403, "text/plain", "forbidden");
      return;
    }

    JsonArray cells = doc["cells"].as<JsonArray>();
    if (cells.isNull() || cells.size() == 0) {
      server.send(400, "text/plain", "no cells");
      return;
    }

    const char* reqId = doc["request_id"] | "";
    const char* lbl = doc["label"] | "";
    Serial.printf("[POST /print-job] accepted request_id=%s label=%s cells=%u\n",
                  reqId, lbl, static_cast<unsigned>(cells.size()));

    PrintHandler::printBrailleCells(cells);

    String out = "{\"ok\":true,\"printed\":";
    out += String(static_cast<unsigned>(cells.size()));
    out += "}";
    server.send(200, "application/json", out);
  }

  inline void init() {
    server.on("/", HTTP_GET, handleRoot);
    server.on("/print", HTTP_GET, handlePrint);
    server.on("/print-job", HTTP_POST, handlePrintJob);
    server.begin();
    Serial.println("HTTP server listening on port 80 ( /, /print?text=&code=, POST /print-job )");
  }
}
