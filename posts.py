#Все что связано с постами
from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, session

posts_bp = Blueprint('posts', __name__)

@posts_bp.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("auth.login"))