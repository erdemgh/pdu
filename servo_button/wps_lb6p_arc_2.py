import serial
import time
import sys

# USB serial bağlantı yolu
usb_serial_path = '/dev/cu.usbserial-142240'


def send_command(ser, *args):
    command = ' '.join(map(str, args)) + '\n'
    ser.write(command.encode())
    time.sleep(1)  # Arduino'nun yanıtı işlemesi için bir süre bekle


def read_response(ser):
    response = ser.readline().decode().strip()
    print("Arduino'dan gelen yanıt:", response)


def main():
    try:
        ser = serial.Serial(usb_serial_path, 9600, timeout=1)
        time.sleep(2)
    except serial.SerialException as e:
        print(f"Hata: {e}")
        return

    if len(sys.argv) > 1:
        try:
            input_args = list(map(int, sys.argv[1:]))

            if len(input_args) == 1:
                press_duration = input_args[0]
                send_command(ser, press_duration)
            elif len(input_args) == 2:
                press_position, press_duration = input_args
                send_command(ser, press_position, press_duration)
            elif len(input_args) == 3:
                press_position, press_duration, release_position = input_args
                send_command(ser, press_position, press_duration, release_position)
            elif len(input_args) == 4:
                press_position, press_duration, release_position, release_duration = input_args
                send_command(ser, press_position, press_duration, release_position, release_duration)
            else:
                print("Hata: Geçersiz argüman sayısı! En fazla 4 argüman girilebilir.")

            read_response(ser)
        except ValueError:
            print("Hata: Geçersiz argümanlar! Argümanlar tam sayı olmalıdır.")
        finally:
            ser.close()
    else:
        print("Hata: Gerekli argümanlar eksik! Script argümanlar ile çalıştırılmalıdır.")


if __name__ == "__main__":
    main()
