import serial
import time


port = '/ttyUSB2'  
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

