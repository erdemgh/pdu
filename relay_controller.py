import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600)
#ser = serial.Serial('/dev/cu.usbserial-142230', 9600)

print("Roleyi açmak için: 1")
print("Roleyi kapatmak için: 0")
print("Röle durumunu sorgulamak için: c")
print("Programdan çıkmak için: q")

while True:
    command = input("Komut girin: ")

    if command.lower() == 'q':
        break

    if command == 'c':
        ser.write(command.encode())
        time.sleep(0.30)
        data = ser.readline()
        print(data.decode())
    elif command in ['0', '1']:
        ser.write(command.encode())
        time.sleep(0.30)
        data = ser.readline()
        print(data.decode())
    else:
        print("Geçersiz komut. Sadece '0', '1', 'c', 'q', veya 'Q' kabul edilir.")

ser.close()
