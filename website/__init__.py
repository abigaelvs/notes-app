from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
import os


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """
    Building the core application of the website
    """

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "avidwkwkland"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note

    create_database(app)

    # Tell flask where the login page
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    """
    Check if the database exist or not
    if database doesn't exists, then create new database
    """
    if not os.path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Database has been created!")