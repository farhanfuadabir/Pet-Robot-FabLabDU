#include <Arduino.h>
#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

////////////////////////////////////////////////////////////////////////////////

#define WLAN_SSID       "Free WiFi"
#define WLAN_PASS       "1988acca"

////////////////////////////////////////////////////////////////////////////////

#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883                   
#define AIO_USERNAME    "atick_iot"
#define AIO_KEY         "98110b48c5334293aa84b194d0b6fd43"
WiFiClient client;

Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);
//////////////////////////////////////////////////////////////////////////////////
Adafruit_MQTT_Publish pet_pub = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/petbot");
Adafruit_MQTT_Subscribe petbot = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/petbot");
//////////////////////////////////////////////////////////////////////////////////
void MQTT_connect();

void setup() {
  Serial.begin(115200);
  delay(10);

  pinMode(2, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);

  Serial.println(F("Adafruit MQTT demo"));
  Serial.println(); Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("WiFi connected");
  Serial.println("IP address: "); Serial.println(WiFi.localIP());
  mqtt.subscribe(&petbot);
}

void loop() {
  MQTT_connect();
  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(5000))) {
    if (subscription == &petbot) {
      Serial.print(F("Got: "));
      Serial.println((char *)petbot.lastread);
      /////////////////////////////////////////////////////////
      int value = atoi((char *)petbot.lastread);
      switch(value){
        case 1:
          digitalWrite(4, HIGH);
          delay(1000);
          digitalWrite(4, LOW);
          delay(1000);
          digitalWrite(4, HIGH);
          delay(1000);
          digitalWrite(4, LOW);
          delay(1000);
          digitalWrite(4, HIGH);
          delay(1000);
          digitalWrite(4, LOW);
          pet_pub.publish(0);
          break;
        case 2:
          digitalWrite(5, HIGH);
          break;
        case 3:
          digitalWrite(4, HIGH);
          break;
        default:
          break;
      }
      /////////////////////////////////////////////////////////
    }
  }
}

void MQTT_connect() {
  int8_t ret;
  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) {
       Serial.println(mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       mqtt.disconnect();
       delay(5000);
       retries--;
       if (retries == 0) {
         while (1);
       }
  }
  Serial.println("MQTT Connected!");
}