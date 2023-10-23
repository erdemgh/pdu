import serial
import time
from flask import Flask, render_template, request

ser = serial.Serial('/dev/ttyUSB0', 9600)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index3.html')  # index2.html kullan


@app.route('/submit', methods=['GET', 'POST'])  # Hem GET hem de POST isteklerini kabul et
def submit():
    if request.method == 'GET':
        command = request.args.get('command')  # GET ile gelen 'command' parametresini
    elif request.method == 'POST':
        command = request.form['command']  # POST ile gelen 'command' parametresini al

    if command.lower() == 'q':
        return "Program sonlandırıldı."
    elif command == 'c':
        ser.write(command.encode())
        time.sleep(0.30)
        data = ser.readline()
        return data.decode()
    elif command in ['0', '1']:
        ser.write(command.encode())
        time.sleep(0.30)
        data = ser.readline()
        return data.decode()
    else:
        return "Geçersiz komut. Sadece '0', '1', 'c' veya 'q' kabul edilir."


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2130)
