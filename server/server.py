from flask import Flask, request
from flask_socketio import SocketIO, send
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')  # В реальном приложении пароль должен быть хеширован

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (email text, password text)''')

    c.execute("INSERT INTO users VALUES (?,?)", (email, password))

    conn.commit()
    conn.close()

    return 'OK', 200

if __name__ == '__main__':
    socketio.run(app)
