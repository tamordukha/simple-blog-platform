#Основная часть приложение. Собирает все приложение и запускает его
from flask import Flask

from auth import auth_bp
from posts import posts_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "something-secret"
app.config["DATABASE"] = "database.db"

app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)

if __name__ == "__main__":
    app.run(debug=True)
