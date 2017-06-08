from flask import request, make_response, jsonify
from functools import wraps

from app.models import User


def auth_token(func):

    @wraps(func)
    def decorator(*args, **kwargs):
        access_token = request.headers.get("Authorization")

        if access_token:
            # decode token and get the User ID
            kwargs["user_id"] = User.decode_token(access_token)
            if not isinstance(kwargs["user_id"], int):
                message = kwargs["user_id"]
                response = {
                    "message": message
                }
                return make_response(jsonify(response)), 401

        return func(*args, **kwargs)
    return decorator
