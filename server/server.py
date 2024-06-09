from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')  # Предполагается, что пароль уже хеширован

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (email text PRIMARY KEY, password text)''')

    c.execute("INSERT INTO users VALUES (?,?)", (email, password))

    # Создание записи в таблице pet_profiles для нового пользователя
    c.execute('''CREATE TABLE IF NOT EXISTS pet_profiles
                 (owner_email text PRIMARY KEY, pet_name text, pet_breed text, pet_birthday text, image_path text)''')

    c.execute("INSERT INTO pet_profiles (owner_email) VALUES (?)", (email,))

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

@app.route('/pet_profile', methods=['GET'])
def pet_profile():
    email = request.args.get('email')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM pet_profiles WHERE owner_email=?", (email,))
    pet_profile = c.fetchone()
    conn.close()
    if pet_profile:
        # Преобразовать кортеж в словарь
        keys = ['owner_email', 'pet_name', 'pet_breed', 'pet_birthday', 'image_path', 'pet_type']  # Добавьте 'pet_type'
        pet_profile_dict = dict(zip(keys, pet_profile))
        print(pet_profile_dict)
        return jsonify(pet_profile_dict), 200
    else:
        return jsonify({"error": "Pet profile not found"}), 404


@app.route('/save_pet_profile', methods=['POST'])
def save_pet_profile():
    data = request.get_json()
    email = data.get('email')
    pet_name = data.get('pet_name')
    pet_breed = data.get('pet_breed')
    owner_email = data.get('owner_email')  # Используйте owner_email
    pet_birthday = data.get('pet_birthday')  # Добавьте pet_birthday
    image_path = data.get('image_path')  # Добавьте image_path
    pet_type = data.get('pet_type')  # Добавьте тип питомца

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Обновить запись в базе данных
    c.execute("UPDATE pet_profiles SET pet_name = ?, pet_breed = ?, pet_birthday = ?, image_path = ?, owner_email = ?, pet_type = ? WHERE owner_email = ?",
              (pet_name, pet_breed, pet_birthday, image_path, owner_email, pet_type, email))  # Добавьте pet_type
    conn.commit()
    conn.close()

    return jsonify({"message": "Pet profile updated successfully"}), 200



if __name__ == '__main__':
    socketio.run(app)
