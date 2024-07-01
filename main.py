import sys
from flask import Flask, request, render_template, redirect, url_for, session
from controller import esp 
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tacko'
socketio = SocketIO(app)
database = "sql.db"

def connect():
    return sqlite3.connect(database)

def room_update(q):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(q)
    connection.commit()
    connection.close()
    # Değişiklik olduğunda room_update olayını tetikle
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        socketio.emit('room_update', {'fire': rooms[0][1], 'door': rooms[0][2], 'move': rooms[0][3]})

def get_phone_number_from_database():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT phone_number FROM phone_numbers WHERE id = 1")
        phone_number = cursor.fetchone()[0]
        return phone_number

@socketio.on('get_room_data')
def get_room_data():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        socketio.emit('room_update', {'fire': rooms[0][1], 'door': rooms[0][2], 'move': rooms[0][3]})

@socketio.on('get_sensor_data')
def get_sensor_data():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sensor_data")
        sensor_data = cursor.fetchall()
        socketio.emit('sensor_update', {'temperature': sensor_data[0][1], 'humidity': sensor_data[0][2]})

@app.route('/')
def index():
    if 'logged_in' in session:
        room_update("SELECT * FROM rooms")
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/open_door', methods=['GET'])
def open_door():
    state = request.args.get('state')
    phone_number = get_phone_number_from_database()
    if state == 'on':
        esp.smm(phone_number, "Serverin Gapysy Acyldy !!!")
        room_update("UPDATE rooms SET door='on' WHERE id=1")
        return 'Door opened\n'
    elif state == 'off':
        esp.smm(phone_number, "Door Closed")
        room_update("UPDATE rooms SET door='off' WHERE id=1")
        return 'Door closed\n'
    else:
        return 'Invalid state\n'


@app.route('/fire_alert', methods=['GET'])
def fire_alert():
    state = request.args.get('state')
    phone_number = get_phone_number_from_database()
    if state == 'on':
        esp.smm(phone_number, "Serverde Yangyn Cykdy !!!!")
        room_update("UPDATE rooms SET fire='on' WHERE id=1")
        return 'Fire detected\n'
    elif state == 'off':
        room_update("UPDATE rooms SET fire='off' WHERE id=1")
        return "No fire detected\n"
    else:
        return 'Invalid state\n'


@app.route("/movement_alert", methods=['GET'])
def movement_alert():
    state = request.args.get('state')
    phone_number = get_phone_number_from_database()
    if state == 'on':
        esp.smm(phone_number, "Serverde Otagynda Hereket Bar !!!!")
        room_update("UPDATE rooms SET move='on' WHERE id=1")
        return 'Movement detected\n'
    elif state == 'off':
        room_update("UPDATE rooms SET move='off' WHERE id=1")
        return 'No movement detected\n'
    else: 
        return 'Invalid state\n'

@app.route('/temperature_humidity', methods=['GET'])
def temperature_humidity():
    temperature = request.args.get('temperature')
    humidity = request.args.get('humidity')

    if temperature is not None and humidity is not None:
        conn = connect()
        c = conn.cursor()
        c.execute("UPDATE sensor_data SET temperature=?, humidity=? WHERE id=1", (temperature, humidity))
        conn.commit()
        socketio.emit('sensor_update', {'temperature': temperature, 'humidity': humidity})
        return "Data updated successfully!"
    else:
        error_msg = "Error: Missing temperature or humidity parameter"
        print(error_msg)
        return error_msg, 400

@app.route('/change_phone_number', methods=['GET', 'POST'])
def change_phone_number():
    if request.method == 'POST':
        new_phone_number = request.form['new_phone_number']
        update_phone_number(new_phone_number)
        return redirect(url_for('index'))
    else:
        current_phone_number = get_phone_number_from_database()
        return render_template('phone_number.html', current_phone_number=current_phone_number)

def update_phone_number(new_phone_number):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE phone_numbers SET phone_number=? WHERE id=1", (new_phone_number,))
        conn.commit()

def get_phone_number_from_database():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT phone_number FROM phone_numbers WHERE id = 1")
        phone_number = cursor.fetchone()[0]
        return phone_number
if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    socketio.run(app, host='0.0.0.0',port=5656)
