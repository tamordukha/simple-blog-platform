#Работа с базой данных, таблицами, SQL
from flask import app
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

from werkzeug.security import generate_password_hash

def register_db(username, password, db_path):
    hashed_password = generate_password_hash(password)

    conn = get_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return "This username is already taken.", 400
    finally:
        conn.close()

def login_db(username, password, db_path):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        return user

    return None

def get_all_posts(db_path):
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts")
    all_posts = cursor.fetchall()
    conn.close
    return all_posts

def get_post(post_id, db_path):
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()

    conn.close()
    return post

def add_post_to_db(user_id, title, content, db_path):
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "INSERT INTO posts (author_id, title, content) VALUES (?, ?, ?)"
    data = (user_id, title, content)
    cursor.execute(query, data)
    conn.commit()
    conn.close()

def change_post_in_db(post_id, title, content, db_path):
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
            UPDATE posts
            SET title = ?, content = ?
            WHERE id = ?
            """
    data = (title, content, post_id)
    cursor.execute(query,data)
    conn.commit()
    conn.close()

def delete_post_from_db(post_id, db_path):
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?",(post_id,))
    conn.commit()
    conn.close()