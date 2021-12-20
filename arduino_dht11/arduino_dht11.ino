#include "includes.h"
#include "config.h"

void setup() {
  initSerial();
  initDHT();
}

void loop() {
  currentMillis = millis();
  sendDhtMessage();
}
