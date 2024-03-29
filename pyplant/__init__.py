from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from pyplant.config import Config
import matplotlib.pyplot as plt


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # app.config.update(ax1=self.ax1, ax=self.ax)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from pyplant.plants.routes import plants
    from pyplant.main.routes import main
    from pyplant.errors.handlers import errors
    from pyplant.users.routes import users
    from pyplant.pots.routes import pots
    app.register_blueprint(main)
    app.register_blueprint(plants)
    app.register_blueprint(pots)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app


# @app.before_first_request
# def create_tables():
#     db.create_all()
