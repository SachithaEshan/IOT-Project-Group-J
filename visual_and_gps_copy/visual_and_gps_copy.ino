#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPS++.h>

const char* ssid = "Galaxy A30s504";
const char* password = "12345678";

// const char* ssid = "SLT_FIBRE";
// const char* password = "Thejan321";

const char* serverHost = "192.168.162.152"; // Replace with your server's IPv4 address
const int serverPort = 8081; // Port number for the server

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
WiFiClient wifiClient;

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
        // Send data to ThingSpeak
        sendToThingSpeak(gps.location.lat(), gps.location.lng(), speed, totalSpeed / sampleCount);
        sendToServer(gps.location.lat(), gps.location.lng(), speed);
      }
    }
  }

  unsigned long currentMillis = millis();
  if (currentMillis - lastUpdateMillis >= 60000) { // Update every 1 minute
    if (sampleCount > 0) {
      float averageSpeed = totalSpeed / sampleCount;
      // Send data to ThingSpeak
      sendToThingSpeak(gps.location.lat(), gps.location.lng(), 0, averageSpeed);
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
  HTTPClient httpClient;
  String postData = "lat=" + String(latitude, 6) + "&lng=" + String(longitude, 6) + "&speed=" + String(speed, 2);

  Serial.println("Sending data to server...");
  if (httpClient.begin(wifiClient, serverHost, serverPort, "/log")) {
    httpClient.addHeader("Content-Type", "application/x-www-form-urlencoded");

    int httpResponseCode = httpClient.POST(postData);
    if (httpResponseCode > 0) {
      Serial.printf("[HTTP] POST request to server succeeded, response code: %d\n", httpResponseCode);
    } else {
      Serial.printf("[HTTP] POST request to server failed, error: %s\n", httpClient.errorToString(httpResponseCode).c_str());
    }
    httpClient.end();
  } else {
    Serial.println("[HTTP] Unable to connect to server");
  }
}

void sendToThingSpeak(float latitude, float longitude, float speed, float averageSpeed) {
  HTTPClient httpClient;

  String url = "http://" + String(thingSpeakAddress) + "/update?api_key=" + thingSpeakAPIKey + "&" +
               thingSpeakFieldLatitude + "=" + String(latitude, 6) + "&" +
               thingSpeakFieldLongitude + "=" + String(longitude, 6) + "&" +
               thingSpeakFieldSpeed + "=" + String(speed, 2) + "&" +
               thingSpeakFieldAverageSpeed + "=" + String(averageSpeed, 2);

  Serial.println("Sending data to ThingSpeak...");
  if (httpClient.begin(url)) {
    int httpResponseCode = httpClient.GET();
    if (httpResponseCode > 0) {
      Serial.printf("[HTTP] GET request to ThingSpeak succeeded, response code: %d\n", httpResponseCode);
    } else {
      Serial.printf("[HTTP] GET request to ThingSpeak failed, error: %s\n", httpClient.errorToString(httpResponseCode).c_str());
    }
    httpClient.end();
  } else {
    Serial.println("[HTTP] Unable to connect to ThingSpeak");
  }
}
