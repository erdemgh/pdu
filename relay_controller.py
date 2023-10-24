import serial
import time

#ser = serial.Serial('/dev/cu.usbserial-142230', 9600)
ser = serial.Serial('/dev/ttyUSB0', 9600)

print("Roleyi kapatmak icin: 1/closed")
print("Roleyi acmak için: 0/open")
print("Role durumunu sorgulamak icin: c/check")
print("Role kullanim tipini gormek icin: t/type")
print("Programdan cikmak icin: q")

while True:
    command = input("Komut girin: ")

    if command.lower() in ['q', 'quit']:
        break

    if command in ['c', 'check']:
        ser.write(command.encode())
        time.sleep(0.30)
        data = ser.readline()
        print(data.decode())
    elif command in ['0', '1', 'open', 'closed']:
        ser.write(command.encode())
        time.sleep(0.30)
        data = ser.readline()
        print(data.decode())
    elif command in ['t', 'type']:
        ser.write(command.encode())
        time.sleep(0.30)
        data = ser.readline()
        print(data.decode())
    else:
        print("Gecersiz komut. Sadece '0/open', '1/closed', 'c/check', 't/type' veya 'q/quit' kabul edilir.")

ser.close()
