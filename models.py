#Работа с базой данных, таблицами, SQL
from flask import app
import sqlite3

def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def register_db(username, password, db_path):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    data = (username, password)
    try:
        cursor.execute(query, data)
        conn.commit()
    except sqlite3.IntegrityError:
        return "This username is already taken.", 400
    finally:
        conn.close()

def login_db(username, password, db_path):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    data = (username, password)
    cursor.execute(query, data)
    user = cursor.fetchone()
    conn.close()
    return user