import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time as tm

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

command = "h"

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    client.subscribe("mqtt/command")

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    command = str(msg.payload)
    if command == "f":
        forward()

    elif command == "r":
        right()

    elif command == "l":
        left()

    elif command == "h":
        halt()

def forward():
    GPIO.output(11, True)
    GPIO.output(13, False)
    GPIO.output(23, True)
    GPIO.output(25, False)

def right():
    GPIO.output(11, True)
    GPIO.output(13, False)
    GPIO.output(23, False)
    GPIO.output(25, True)

def left():
    GPIO.output(11, False)
    GPIO.output(13, True)
    GPIO.output(23, True)
    GPIO.output(25, False)

def halt():
    GPIO.output(11, False)
    GPIO.output(13, False)
    GPIO.output(23, False)
    GPIO.output(25, False)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.113", 1883, 60)

client.loop_forever()
