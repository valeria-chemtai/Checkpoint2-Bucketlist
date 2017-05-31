from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

# initializing sqlalchemy
db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(config["config_name"])
