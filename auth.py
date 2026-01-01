#Работа с сессией, маршруты
from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, session
from models import get_connection, register_db, login_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/regist", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db_path = current_app.config['DATABASE']
        register_db(username, password, db_path)

        return redirect("/login")
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db_path = current_app.config['DATABASE']
        user = login_db(username, password, db_path)
        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect("/")
        
        return "Incorrect password or username"
    
    return render_template("login.html")