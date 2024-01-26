import serial
import time
import sys

#usb_serial_path = '/dev/cu.usbserial-142240'  #macos path
usb_serial_path = '/dev/ttyUSB0'

def send_command(ser, press_duration):
    command = f"{press_duration}\n"
    ser.write(command.encode())
    time.sleep(1)

def read_response(ser):
    response = ser.readline().decode().strip()
    print("Arduino'dan gelen yanıt:", response)

def main():
    ser = None
    try:
        ser = serial.Serial(usb_serial_path, 9600, timeout=1)
        time.sleep(2)
        press_duration = int(sys.argv[1])
        send_command(ser, press_duration)
        read_response(ser)
    except (serial.SerialException, ValueError, IndexError) as e:
        print(f"Hata: {e}")
    finally:
        if ser is not None and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
