import serial
import time
from flask import Flask, render_template, request

ser = serial.Serial('/dev/cu.usbserial-142230', 9600)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    command = request.form['command']

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
        return "Geçersiz komut. Sadece '0', '1', 'c', 'q', veya 'Q' kabul edilir."

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=42230)
