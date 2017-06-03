# /app/auth/views.py

from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User


class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        # Query to see if the user already exists
        user_email = User.query.filter_by(email=request.data["email"]).first()
        user_username = User.query.filter_by(
            email=request.data["username"]).first()
        user = user_email or user_username

        if not user:
            try:
                post_data = request.data
                # Register user
                username = post_data["username"]
                email = post_data["email"]
                password = post_data["password"]
                user = User(username=username, email=email, password=password)
                user.save()

                response = {"message": "Successfully Registered"}
                return make_response(jsonify(response)), 201

            except Exception as e:
                response = {
                    "message": str(e)
                }
                return make_response(jsonify(response)), 401

        else:
            response = {"message": "Already Resgistered. Login Please"}
            return make_response(jsonify(response)), 202


# API resource
registration_view = RegistrationView.as_view("register_view")
# Rule for registration with blueprint
auth_blueprint.add_url_rule("/auth/register", view_func=registration_view,
                            methods=["POST"])
