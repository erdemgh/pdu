from flask import Flask, render_template, request, redirect, url_for
import serial
import time

app = Flask(__name__)

def list_serial_ports():
    """List all available serial ports."""
    import serial.tools.list_ports
    return [port.device for port in serial.tools.list_ports.comports()]

# Default password
PASSWORD = "osman"

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
        password = request.form.get("password")
        if password == PASSWORD:
            try:
                selected_port = request.form["serial_port"]
                press_duration = int(request.form["press_duration"])
                ser = serial.Serial(selected_port, 9600, timeout=1)
                time.sleep(2)
                send_command(ser, press_duration)
                response = read_response(ser)
                ser.close()
                return render_template("index.html", response=response, serial_ports=list_serial_ports())
            except (serial.SerialException, ValueError):
                return render_template("index.html", error="Hata: Geçersiz giriş.", serial_ports=list_serial_ports())
        else:
            return render_template("index.html", error="Hata: Yanlış şifre.", serial_ports=list_serial_ports())
    return render_template("index.html", serial_ports=list_serial_ports())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
