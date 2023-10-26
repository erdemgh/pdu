import serial
import time
from flask import Flask, render_template, request
import threading

ser = serial.Serial('/dev/ttyUSB0', 9600)
#ser = serial.Serial('/dev/cu.usbserial-142230', 9600)

app = Flask(__name__)

ip_address = '0.0.0.0'
port = 2135

lock = threading.Lock()

@app.route('/')
def index():
    return render_template('pdu.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        command = request.args.get('command')
    elif request.method == 'POST':
        command = request.form['command']

    command_map = {
        'q': 'Program terminated.',
        'quit': 'Program terminated.',
        'c': 'c',
        'check': 'c',
        '0': '0',
        '1': '1',
        'open': '1',
        'closed': '0',
        't': 't',
        'type': 't',
    }

    command_response = command_map.get(command.lower(),
                                       "Invalid command. Only '0/open', '1/closed', 'c/check', t/type, or 'q/quit' are accepted.")

    if command_response == "Program terminated.":
        return command_response
    else:
        with lock:
            ser.write(command_response.encode())
            time.sleep(0.3)
            data = ser.readline()
        return data.decode()

if __name__ == '__main__':
    app.run(debug=True, host=ip_address, port=port)
