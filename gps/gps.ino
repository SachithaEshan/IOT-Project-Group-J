#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPS++.h>

// const char* WIFI_SSID = "Galaxy A30s504";
// const char* WIFI_PASS = "12345678";

const char* ssid = "SLT_FIBRE";
const char* password = "Thejan321";
const char* host = "192.168.81.152"; // Replace with your laptop's IPv4 address

#define NEO_6M_BAUDRATE 9600
#define NEO_6M_RX_PIN 16
#define NEO_6M_TX_PIN 17

TinyGPSPlus gps;
WiFiClient client;

void setup() {
  Serial.begin(115200);
  Serial1.begin(NEO_6M_BAUDRATE, SERIAL_8N1, NEO_6M_RX_PIN, NEO_6M_TX_PIN);

  connectToWiFi();
}

void loop() {
  while (Serial1.available() > 0) {
    if (gps.encode(Serial1.read())) {
      if (gps.location.isValid() && gps.speed.isValid()) {
        sendToServer(gps.location.lat(), gps.location.lng(), gps.speed.kmph());
      }
    }
  }
}

void connectToWiFi() {
  Serial.println("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

void sendToServer(float latitude, float longitude, float speed) {
  HTTPClient http;
  String postData = "lat=" + String(latitude, 6) + "&lng=" + String(longitude, 6) + "&speed=" + String(speed, 2);

  Serial.println("Sending data to server...");
  if (http.begin("http://" + String(host) + ":8081/log")) { // Change the port number
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    int httpResponseCode = http.POST(postData);
    if (httpResponseCode > 0) {
      Serial.printf("[HTTP] POST request to server succeeded, response code: %d\n", httpResponseCode);
    } else {
      Serial.printf("[HTTP] POST request to server failed, error: %s\n", http.errorToString(httpResponseCode).c_str());
    }
    http.end();
  } else {
    Serial.println("[HTTP] Unable to connect to server");
  }
}
