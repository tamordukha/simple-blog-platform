# Simple Blog Platform (Flask)

A simple blog platform built with Flask to practice authentication, roles,
access control, and CRUD operations.

## Features
- User registration and login
- Session-based authentication
- User roles: user / admin
- Create, read, update, delete blog posts
- Public post listing
- Access control (author or admin only)
- Password hashing
- Automated tests with pytest

## Tech Stack
- Python
- Flask
- Jinja2
- SQLite
- pytest

## Project Structure
app.py
auth.py
posts.py
models.py
templates/
static/
tests/
database.db

## Setup
```bash
pip install -r requirements.txt
python app.py
```

## Run Tests
```bash
pytest
```

## Notes
This project demonstrates core backend concepts such as authentication,
authorization, database relations, and testing.
