import sys
from flask import Flask, request
import time
import serial


port = '/dev/ttyUSB0'  
baudrate = 115200  
def send_sms(port, baudrate, number, message):
    try:   
        ser = serial.Serial(port, baudrate, timeout=1)   
        ser.write('AT+CMGF=1\r\n'.encode())  
        time.sleep(1)
        ser.write('AT+CMGS="{}"\r\n'.format(number).encode())  
        time.sleep(1)
        ser.write('{}\r\n'.format(message).encode())  
        time.sleep(1)
        ser.write(chr(26).encode())  
        time.sleep(1)
        response = ser.readlines()
        print("Modemden status:")
        for line in response:
            print(line.decode().strip())

        ser.close()
    except Exception as e:
        print("SMS gitmedi:", str(e))



def smm(nom,sms):
    port = '/dev/ttyUSB0'  
    baudrate = 115200  
    send_sms(port, baudrate, nom, sms)
