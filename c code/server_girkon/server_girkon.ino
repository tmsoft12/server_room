#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>

const char* ssid     = "TP-Link_66E1";
const char* password = "qwerty12345";
const char* serverUrl = "http://192.168.0.105:5656/";

const int doorPin = 14;
const int pirPin = 12;
const int buzzerPin = 2;

bool doorFlag = false;
bool pirFlag = false;

void setup() {
    Serial.begin(115200);

    pinMode(doorPin, INPUT);
    pinMode(buzzerPin, OUTPUT);
    pinMode(pirPin, INPUT);

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
}

void loop() {
    checkDoor();
    checkMovement();
}

void checkDoor() {
    int doorState = digitalRead(doorPin);
    if (doorState == LOW && !doorFlag) {
        Serial.println("Door opened");
        sendRequest("open_door", "on");
        activateAlarm();
        deactivateAlarm();
        doorFlag = true;
    } else if (doorState == HIGH && doorFlag) {
        sendRequest("open_door", "off");
        doorFlag = false;
        Serial.println("Door closed");
    }
    delay(100);
}

void checkMovement() {
    int pirPinState = digitalRead(pirPin);
    if (pirPinState == LOW && !pirFlag) {
        Serial.println("Movement detected");
        sendRequest("movement_alert", "on");
        activateAlarm();
        deactivateAlarm();
        pirFlag = true;
    } else if (pirPinState == HIGH && pirFlag) {
        sendRequest("movement_alert", "off");
        pirFlag = false;
        Serial.println("Movement stopped");
    }
    delay(100);
}

void sendRequest(const char* endpoint, const char* state) {
    String url = serverUrl;
    url += endpoint;
    url += "?state=";
    url += state;

    WiFiClient client;
    HTTPClient http;
    http.begin(client, url);

    int httpResponseCode = http.GET();
    if (httpResponseCode > 0) {
        Serial.print("HTTP response code: ");
        Serial.println(httpResponseCode);
    }

    http.end();
}

void activateAlarm() {
    tone(buzzerPin, 1000);
}

void deactivateAlarm() {
    noTone(buzzerPin);
}
