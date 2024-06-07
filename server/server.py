from flask import Flask, request, jsonify
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

    # # Создаем запись в таблице pet_profile_info при регистрации
    # c.execute('''CREATE TABLE IF NOT EXISTS pet_profile_info
    #              (pet_name text, breed text, owner text , birthday text, image_path text)''')

    c.execute("INSERT INTO pet_profile_info (owner) VALUES (?)", (email,))

    conn.commit()
    conn.close()

    return 'OK', 200

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')  # В реальном приложении пароль должен быть хеширован

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()

    if user is None:
        return 'Пользователь не найден', 404

    if user[1] != password:
        return 'Неверный пароль', 401

    return 'OK', 200


if __name__ == '__main__':
    socketio.run(app)
