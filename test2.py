import sqlite3

def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Создание таблицы
    c.execute('''
        CREATE TABLE pet_profiles (
            owner_email TEXT PRIMARY KEY,
            pet_name TEXT,
            pet_breed TEXT,
            pet_birthday TEXT,
            image_path TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
