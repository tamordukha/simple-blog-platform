#Все что связано с постами
from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, session, abort
from models import get_all_posts, get_post, add_post_to_db

posts_bp = Blueprint('posts', __name__)

@posts_bp.route("/")
def index():
    db_path = current_app.config['DATABASE']
    posts = get_all_posts(db_path)

    if posts is None:
        abort(404)

    return render_template("index.html", posts=posts)

@posts_bp.route("/post/<int:post_id>")
def show_post(post_id):
    db_path = current_app.config["DATABASE"]
    post = get_post(post_id, db_path)

    if post is None:
        print("I LOVE BURGER")
        abort(404)
    
    user = session
    return render_template("post.html", post=post, user=user)

@posts_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    user_id = session["user_id"]

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        db_path = current_app.config["DATABASE"]
        add_post_to_db(user_id, title, content, db_path)
        return redirect(url_for("posts.index"))
    
    return render_template("create.html")
    
@posts_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("posts.index"))