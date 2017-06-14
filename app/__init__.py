# app/__init__.py
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # import the authentication blueprint and register it on the app
    from .views import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views import bucketlist_blueprint
    app.register_blueprint(bucketlist_blueprint)

    from .views import bucketlist_item_blueprint
    app.register_blueprint(bucketlist_item_blueprint)

    return app
