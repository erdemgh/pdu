from flask import Flask, render_template, request
import serial
import time

app = Flask(__name__)

# usb_serial_path = '/dev/cu.usbserial-142240'  # macos path
usb_serial_path = '/dev/ttyUSB0'

def send_command(ser, press_duration):
    command = f"{press_duration}\n"
    ser.write(command.encode())
    time.sleep(1)

def read_response(ser):
    response = ser.readline().decode().strip()
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            press_duration = int(request.form["press_duration"])
            ser = serial.Serial(usb_serial_path, 9600, timeout=1)
            time.sleep(2)
            send_command(ser, press_duration)
            response = read_response(ser)
            ser.close()
            return render_template("index.html", response=response)
        except (serial.SerialException, ValueError):
            return render_template("index.html", error="Hata: Geçersiz giriş.")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
