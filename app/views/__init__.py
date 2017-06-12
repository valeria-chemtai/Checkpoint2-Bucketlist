# app/views/__init__.py

from flask import Blueprint

# Instance of a Blueprint for the authentication blueprint
auth_blueprint = Blueprint("auth", __name__)
from . import auth

bucketlist_blueprint = Blueprint("bucketlist", __name__)
from . import bucketlist


bucketlist_item_blueprint = Blueprint("bucketlist_item", __name__)
from . import bucketlist_item
