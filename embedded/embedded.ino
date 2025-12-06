/*
    Simple ground station receiver / transmitter for use with Elven Aerospace Industries products
    Copyright (C) 2025  Rowan Zhang

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 3 as published by
    the Free Software Foundation

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, see <https://www.gnu.org/licenses/>.
*/

#include <Arduino.h> // LGPLv2.1
#include <LoRa.h>    // MIT

int radioFreq = 0;
String FW_VERSION = "Elven Aerospace Industries Wireless Dongle Firmware version v1.0 (Ground Station)";

void setup() {
  Serial.begin(115200);
  pinMode(PC13, OUTPUT);
  digitalWrite(PC13, 1);
  
  while (!Serial);

  Serial.println("Elven Aerospace Industries Ground Station Dongle");

  // Frequency selection
  while ((radioFreq < 430E6) or (radioFreq > 440E6)) {
    Serial.println("Please enter a frequency between 430000000Hz, and 440000000Hz");
    while (!Serial.available()) {}
    radioFreq = Serial.readStringUntil('\n').toInt();
  }
  Serial.print("Radio frequency set to: ");
  Serial.println(radioFreq);
  
  // Radio setup
  LoRa.setPins(PA8, PB2, -1);
  if (!LoRa.begin(radioFreq)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

bool LED = true;
int timer = 0;

void loop() {
  // Receive data
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    Serial.print("RECV:");
    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }
    Serial.print("RSSI:");
    Serial.println(LoRa.packetRssi());
  }

  // Transmit if there is data on serial port
  if (Serial.available()) {
    String dataToSend = Serial.readStringUntil('\n');
    if (dataToSend.indexOf("about") > -1) {
      Serial.println(FW_VERSION);
    }
    else {
      Serial.print("Sending:");
      Serial.println(dataToSend);
      LoRa.beginPacket();
      LoRa.print(dataToSend);
      LoRa.endPacket();
    }
  }

  if ((millis() - timer) > 1000) {
    LED = !LED;
    timer = millis();
  }

  digitalWrite(PC13, LED);
}
