# app/auth/__init__.py

from flask import Blueprint

# Instance of a Blueprint for the authentication blueprint
auth_blueprint = Blueprint("auth", __name__)

from . import views
