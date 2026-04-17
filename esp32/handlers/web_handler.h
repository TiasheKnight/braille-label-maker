#pragma once

#include <WebServer.h>
#include <Arduino.h>

extern WebServer server;

namespace WebHandler {
  inline void handleRoot();
  inline void handlePrint();
  inline void init();
}

#include "../components/braille.h"
#include "print_handler.h"

namespace WebHandler {
  inline void handleRoot() {
    String html = R"rawliteral(
      <html>
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Braille Label Maker</title>
          <style>body{font-family:Arial,sans-serif;margin:24px;}input{width:90%;padding:10px;}button{padding:10px 16px;}</style>
        </head>
        <body>
          <h2>Braille Label Maker</h2>
          <form action="/print" method="GET">
            <input name="text" placeholder="Enter text" autocomplete="off" />
            <button type="submit">Print</button>
          </form>
        </body>
      </html>
    )rawliteral";
    server.send(200, "text/html", html);
  }

  inline void handlePrint() {
    if (!server.hasArg("text")) {
      server.send(400, "text/plain", "Missing text");
      return;
    }
    String text = server.arg("text");
    PrintHandler::printText(text);
    String response = "<html><body><p>Printed: " + text + "</p><p><a href=\"/\">Back</a></p></body></html>";
    server.send(200, "text/html", response);
  }

  inline void init() {
    server.on("/", handleRoot);
    server.on("/print", handlePrint);
    server.begin();
    Serial.println("Web server listening");
  }
}
