#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPS++.h>

// const char* ssid = "SLT_FIBRE";
// const char* password = "Thejan321";

const char* ssid = "Galaxy A30s504";
const char* password = "12345678";

// const char* ssid = "Galaxy A015902";
// const char* password = "amcmsc123";

const char* thingSpeakAddress = "api.thingspeak.com";
const String thingSpeakAPIKey = "G9OQNE6EF0O9VPE0";
const String thingSpeakFieldLatitude = "field1"; // Field for latitude data
const String thingSpeakFieldLongitude = "field2"; // Field for longitude data
const String thingSpeakFieldSpeed = "field3"; // Field for speed data
const String thingSpeakFieldAverageSpeed = "field4"; // Field for average speed data

#define NEO_6M_BAUDRATE 9600
#define NEO_6M_RX_PIN 16
#define NEO_6M_TX_PIN 17

TinyGPSPlus gps;
WiFiClient client;

unsigned long lastUpdateMillis = 0;
float totalSpeed = 0.0;
int sampleCount = 0;

void setup() {
  Serial.begin(115200);
  Serial1.begin(NEO_6M_BAUDRATE, SERIAL_8N1, NEO_6M_RX_PIN, NEO_6M_TX_PIN);
  connectToWiFi();
}

void loop() {
  while (Serial1.available() > 0) {
    if (gps.encode(Serial1.read())) {
      if (gps.location.isValid() && gps.speed.isValid()) {
        float speed = gps.speed.kmph();
        totalSpeed += speed;
        sampleCount++;
        sendToServer(gps.location.lat(), gps.location.lng(), speed);
        sendToThingSpeak(gps.location.lat(), gps.location.lng(), speed);
      }
    }
  }

  unsigned long currentMillis = millis();
  if (currentMillis - lastUpdateMillis >= 60000) { // Update every 1 minute
    if (sampleCount > 0) {
      float averageSpeed = totalSpeed / sampleCount;
      sendAverageSpeedToThingSpeak(averageSpeed);
      totalSpeed = 0.0;
      sampleCount = 0;
    }
    lastUpdateMillis = currentMillis;
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
  // Send data to your server
}

void sendToThingSpeak(float latitude, float longitude, float speed) {
  HTTPClient http;

  String url = "http://" + String(thingSpeakAddress) + "/update?api_key=" + thingSpeakAPIKey + "&" +
               thingSpeakFieldLatitude + "=" + String(latitude, 6) + "&" +
               thingSpeakFieldLongitude + "=" + String(longitude, 6) + "&" +
               thingSpeakFieldSpeed + "=" + String(speed, 2);

  Serial.println("Sending data to ThingSpeak...");
  if (http.begin(url)) {
    int httpResponseCode = http.GET();
    if (httpResponseCode > 0) {
      Serial.printf("[HTTP] GET request to ThingSpeak succeeded, response code: %d\n", httpResponseCode);
    } else {
      Serial.printf("[HTTP] GET request to ThingSpeak failed, error: %s\n", http.errorToString(httpResponseCode).c_str());
    }
    http.end();
  } else {
    Serial.println("[HTTP] Unable to connect to ThingSpeak");
  }
}

void sendAverageSpeedToThingSpeak(float averageSpeed) {
  HTTPClient http;

  String url = "http://" + String(thingSpeakAddress) + "/update?api_key=" + thingSpeakAPIKey + "&" +
               thingSpeakFieldAverageSpeed + "=" + String(averageSpeed, 2);

  Serial.println("Sending average speed to ThingSpeak...");
  if (http.begin(url)) {
    int httpResponseCode = http.GET();
    if (httpResponseCode > 0) {
      Serial.printf("[HTTP] GET request to ThingSpeak succeeded, response code: %d\n", httpResponseCode);
    } else {
      Serial.printf("[HTTP] GET request to ThingSpeak failed, error: %s\n", http.errorToString(httpResponseCode).c_str());
    }
    http.end();
  } else {
    Serial.println("[HTTP] Unable to connect to ThingSpeak");
  }
}
