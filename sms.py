import serial
import time

def send_sms(serial_port, phone_number, message):
    # Seri port uzerinden iletisim kur
    ser = serial.Serial(serial_port, 9600, timeout=1)

    # Modem haz?r olana kadar bekle
    time.sleep(2)

    # AT komutlar?yla modemle iletisim kur
    ser.write(b'AT\r')
    response = ser.read(100).decode('utf-8')
    print(response)

    # SMS gonderme moduna gec
    ser.write(b'AT+CMGF=1\r')
    response = ser.read(100).decode('utf-8')
    print(response)

    # Al?c? numaras?n? belirt
    ser.write(f'AT+CMGS="{phone_number}"\r'.encode('utf-8'))
    time.sleep(1)

    # Mesaj? gonder
    ser.write(f'{message}\r'.encode('utf-8'))
    time.sleep(1)

    # CTRL+Z ile SMS gondermeyi bitir
    ser.write(b'\x1A')
    time.sleep(1)

    # Cevab? oku (SMS gonderme durumu)
    response = ser.read(100).decode('utf-8')
    print(response)

    # Seri portu kapat
    ser.close()

# SMS gonderme islemi
if __name__ == "__main__":
    # Seri port (ornegin, Windows'ta COM3, Linux'ta /dev/ttyUSB0)
    serial_port = "/dev/ttyUSB0"

    # Al?c? telefon numaras?
    phone_number = "+99362805208"  # Buraya hedef telefon numaras?n? girin

    # Gonderilecek mesaj
    message = "salam"

    # SMS gonderme fonksiyonunu cag?r
    send_sms(serial_port, phone_number, message)
