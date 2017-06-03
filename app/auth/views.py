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


class LoginView(MethodView):
    """This class handles user login and access token generation."""

    def post(self):
        user_email = User.query.filter_by(email=request.data["email"]).first()
        user_username = User.query.filter_by(
            email=request.data["username"]).first()
        user = user_email or user_username

        try:
            if user and user.password_is_valid(request.data['password']):
                # Generate access token to be used as authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        "message": "Login Successful",
                        "access_token": access_token.decode()
                    }
                    return make_response(jsonify(response)), 200

            else:
                response = {
                    "message": "email/username unkown. Register to continue"}
                return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                "message": str(e)
            }
            return make_response(jsonify(response)), 500


# API resource
registration_view = RegistrationView.as_view("register_view")
login_view = LoginView.as_view("login_view")
# Rule for registration with blueprint
auth_blueprint.add_url_rule("/auth/register", view_func=registration_view,
                            methods=["POST"])
# Rule for login with blueprint
auth_blueprint.add_url_rule("/auth/login", view_func=login_view,
                            methods=["POST"])
