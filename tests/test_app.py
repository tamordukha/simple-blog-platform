import pytest
import sqlite3
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask.testing import FlaskClient

@pytest.fixture

def client():
    app.config["TESTING"] = True
    app.config["DATABASE"] = "test.db"
    app.config["SECRET_KEY"] = "test-secret"

    with app.test_client() as client:
        yield client

def test_register(client: FlaskClient):
    response = client.post("/regist", data={"username": "Saulgoodman", "password": "bingo"})
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", ("Saulgoodman",))
    user = cursor.fetchone()
    conn.close()

    assert user is not None
    assert response.status_code == 302

def test_login(client: FlaskClient):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    hashed_password = generate_password_hash("test_password")
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    data = ("test_username12", hashed_password)
    cursor.execute(query, data)
    conn.commit()
    conn.close()

    response = client.post("/login", data={"username": "test_username12", "password": "test_password"})
    assert response.status_code == 302
    with client.session_transaction() as sess:
        assert "user_id" in sess

def test_login_wrong_password(client: FlaskClient):
    client.post("/register", data={
        "username": "test_user4",
        "password": "correct_password"
    })

    response = client.post("/login", data={
        "username": "test_user4",
        "password": "wrong_password"
    })

    assert response.status_code == 200
    assert b"Incorrect" in response.data

def test_guest_cannot_create_post(client: FlaskClient):
    response = client.post("/post/create", data={
        "title": "test",
        "content": "test"
    })

    assert response.status_code in (302, 401, 403)


def test_user_can_create_post(client: FlaskClient):
    client.post("/regist", data={
        "username": "user1",
        "password": "1234"
    })

    client.post("/login", data={
        "username": "user1",
        "password": "1234"
    })

    response = client.post("/post/create", data={
        "title": "test title",
        "content": "test content"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"test title" in response.data


def test_user_cannot_edit(client: FlaskClient):
    client.post("/regist", data={
        "username": "user2",
        "password": "1234"
    })

    client.post("/login", data={
        "username": "user2",
        "password": "1234"
    })

    response = client.post("/post/create", data={
        "title": "TITLE test cannot edit",
        "content": "CONTENT test cannot edit"
    }, follow_redirects=True)

    client.get("/logout")

    client.post("/regist", data={
        "username": "user3",
        "password": "1234"
    })

    client.post("/login", data={
        "username": "user3",
        "password": "1234"
    })

    response = client.post("/post/edit", data={
        "title": "TITLE test cannot edit (nah i can)",
        "content": "CONTENT test cannot edit (nah i can)"
    }, follow_redirects=True)
    assert response.status_code == 404


def test_view_posts_public(client: FlaskClient):
    client.post("/regist", data={
        "username": "user3",
        "password": "1234"
    })
    client.post("/login", data={
        "username": "user3",
        "password": "1234"
    })
    client.post("/post/create", data={
        "title": "Public post",
        "content": "Visible"
    })
    client.get("/logout")

    response = client.get("/")

    assert response.status_code == 200
    assert b"Public post" in response.data
