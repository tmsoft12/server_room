#include <ESP8266WiFi.h>
#include <WiFiManager.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

const char* fireUrl = "http://192.168.12.1:5656/fire_alert";
const char* serverUrl = "http://192.168.12.1:5656/temperature_humidity";
const int buzzerPin = 2;
const int firePin = 14;
bool fireFlag = false;

#define DHTPIN 12
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

float lastTemperature = 0.0;
float lastHumidity = 0.0;

WiFiManager wifiManager;

void setup() {
    Serial.begin(115200);
    pinMode(firePin, INPUT);

    wifiManager.autoConnect("tm");
    Serial.println("Connected to WiFi");

    dht.begin();

    Serial.println("WiFi connected");
}

void loop() {
    checkFireSensor();
    readTemperatureHumidity();

    // Add other tasks here

    delay(5000); // Consider using non-blocking techniques
}

void checkFireSensor() {
    int fireState = digitalRead(firePin);
    if (fireState == LOW && !fireFlag) {
        Serial.println("Fire detected");
        sendFireAlert("on");
        activateAlarm(); 
        fireFlag = true;
    }
    else if (fireState == HIGH && fireFlag) {
        Serial.println("Fire closed");
        sendFireAlert("off");
        deactivateAlarm(); 
        fireFlag = false;
    }
}

void readTemperatureHumidity() {
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    if (isnan(humidity) || isnan(temperature)) {
        Serial.println("Failed to read from DHT sensor!");
        return;
    }

    if (temperature != lastTemperature || humidity != lastHumidity) {
        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.print(" °C, Humidity: ");
        Serial.print(humidity);
        Serial.println("%");

        sendDataToServer(temperature, humidity);

        lastTemperature = temperature;
        lastHumidity = humidity;
    }
}

void sendFireAlert(const char* state) {
    WiFiClient client;
    HTTPClient http;
    String url = String(fireUrl) + "?state=" + String(state);
    if (!http.begin(client, url)) {
        Serial.println("Failed to connect to fire server!");
        return;
    }
    int httpResponseCode = http.GET();
    if (httpResponseCode > 0) {
        Serial.print("Fire HTTP response code: ");
        Serial.println(httpResponseCode);
    }
    else {
        Serial.println("Fire HTTP request failed!");
    }
    http.end();
}

void sendDataToServer(float temperature, float humidity) {
    WiFiClient client;
    HTTPClient http;

    String url = String(serverUrl) + "?temperature=" + String(temperature) + "&humidity=" + String(humidity);

    if (!http.begin(client, url)) {
        Serial.println("Failed to connect to server!");
        return;
    }
    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
        Serial.print("Server HTTP response code: ");
        Serial.println(httpResponseCode);
    }
    else {
        Serial.println("Server HTTP request failed!");
    }

    http.end();
}
void activateAlarm() {
    tone(buzzerPin, 1000); 
}

void deactivateAlarm() {
    noTone(buzzerPin); 
}
