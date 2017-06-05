# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response


# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import User, BucketList, BucketListItem

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.route("/bucketlists/", methods=["POST", "GET"])
    def bucketlists():
        # Get the access token from the header
        auth_header = request.headers.get("Authorization")
        access_token = auth_header.split(" ")[1]

        if access_token:
            # decode token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):

                # POST bucketlist by for user
                if request.method == "POST":
                    name = str(request.data.get("name", ""))
                    if name:
                        bucketlist = BucketList(name=name, created_by=user_id)
                        bucketlist.save()
                        response = jsonify({
                            "id": bucketlist.id,
                            "name": bucketlist.name,
                            "date_created": bucketlist.date_created,
                            "date_modified": bucketlist.date_modified,
                            "created_by": user_id
                        })
                        return make_response(response), 201

                else:
                    # GET all bucketlist by user
                    bucketlists = BucketList.query.filter_by(
                        created_by=user_id)
                    results = []

                    for bucketlist in bucketlists:
                        details = {
                            "id": bucketlist.id,
                            "name": bucketlist.name,
                            "date_created": bucketlist.date_created,
                            "date_modified": bucketlist.date_modified,
                            "created_by": bucketlist.created_by
                        }
                        results.append(details)
                    return make_response(jsonify(results)), 200
            else:
                # unregistered user
                message = user_id
                response = {
                    "message": message
                }
                return make_response(jsonify(response)), 401

    @app.route("/bucketlists/<int:id>", methods=["GET", "PUT", "DELETE"])
    def bucketlist_manipulation(id, **kwargs):
        # get the access token from the header
        auth_header = request.headers.get("Authorization")
        access_token = auth_header.split(" ")[1]

        if access_token:
            # decode token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # Get the bucketlist with the id specified from the URL
                bucketlist = BucketList.query.filter_by(id=id).first()

                if not bucketlist:
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == "PUT":
                    # Update bucketlist with new name
                    name = str(request.data.get("name", ""))

                    bucketlist.name = name
                    bucketlist.save()

                    response = {
                        "id": bucketlist.id,
                        "name": bucketlist.name,
                        "date_created": bucketlist.date_created,
                        "date_modified": bucketlist.date_modified,
                        "created_by": bucketlist.created_by
                    }
                    return make_response(jsonify(response)), 200

                elif request.method == "GET":
                    # Fetch the specified bucketlist
                    response = {
                        "id": bucketlist.id,
                        "name": bucketlist.name,
                        "date_created": bucketlist.date_created,
                        "date_modified": bucketlist.date_modified,
                        "created_by": bucketlist.created_by
                    }
                    return make_response(jsonify(response)), 200

                else:
                    # request.method == "DELETE"
                    # delete the bucketlist using our delete method
                    bucketlist.delete()
                    return {"message": "bucketlist {} deleted".
                            format(bucketlist.id)}, 200

            else:
                # Unregistered User
                message = user_id
                response = {"message": message}
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401

    @app.route("/bucketlists/<int:id>/items/", methods=["POST"])
    def bucketlist_item(id, **kwargs):
        auth_header = request.headers.get("Authorization")
        access_token = auth_header.split(" ")[1]

        if access_token:
            # decode token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):

                bucketlist = BucketList.query.filter_by(id=id).first()

                if not bucketlist:
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == "POST":
                    name = str(request.data.get("name", ""))
                    if name:
                        item = BucketListItem(name=name, bucketlist_id=id)
                        item.save()
                        response = jsonify({
                            "id": item.id,
                            "name": item.name,
                            "date_created": item.date_created,
                            "date_modified": item.date_modified,
                            "bucketlist_id": id
                        })
                        return make_response(response), 201

        # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
