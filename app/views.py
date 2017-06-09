# app/__init__.py
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

from instance.config import app_config


# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    import decorator
    from app.models import BucketList, BucketListItem

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.route("/bucketlists/", methods=["POST", "GET"])
    @decorator.auth_token
    def bucketlists(*args, **kwargs):
        user_id = kwargs["user_id"]
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

    @app.route("/bucketlists/<int:id>", methods=["GET", "PUT", "DELETE"])
    @decorator.auth_token
    def bucketlist_manipulation(id, *args, **kwargs):
        # get the access token from the header
        # Get the bucketlist with the id specified from the URL
        user_id = kwargs["user_id"]
        bucketlist = BucketList.query.filter_by(
            id=id, created_by=user_id).first()
        # filter bucketlist with id and user_id
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
            related_items = BucketListItem.query.filter_by(
                bucketlist_id=id)
            results = []
            for item in related_items:
                details = {
                    "id": item.id,
                    "name": item.name,
                    "date_created": item.date_created,
                    "date_modified": item.date_modified,
                    "done": item.done
                }
                results.append(details)
            response = {
                "id": bucketlist.id,
                "name": bucketlist.name,
                "items": results,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified,
                "created_by": bucketlist.created_by
            }
            return make_response(jsonify(response)), 200

        else:
            # delete the bucketlist using our delete method
            bucketlist.delete()
            return {"message": "bucketlist {} deleted".
                    format(bucketlist.id)}, 200

    @app.route("/bucketlists/<int:id>/items/", methods=["POST"])
    @decorator.auth_token
    def bucketlist_item(id, **kwargs):
        user_id = kwargs["user_id"]
        bucketlist = BucketList.query.filter_by(
            id=id, created_by=user_id).first()

        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        else:
            name = str(request.data.get("name", ""))
            if name:
                item = BucketListItem(name=name, bucketlist_id=id)
                item.save()
                response = jsonify({
                    "id": item.id,
                    "name": item.name,
                    "date_created": item.date_created,
                    "date_modified": item.date_modified,
                    "bucketlist_id": id,
                    "done": item.done
                })
                return make_response(response), 201

    @app.route("/bucketlists/<int:id>/items/<int:item_id>",
               methods=["PUT", "GET", "DELETE"])
    @decorator.auth_token
    def bucketlist_item_manipulation(id, item_id, **kwargs):
        user_id = kwargs["user_id"]
        bucketlist = BucketList.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        else:
            item = BucketListItem.query.filter_by(id=item_id).first()
            if not item:
                # Raise an HTTPException
                abort(404)

            if request.method == "PUT":
                # Update bucketlist with new name
                name = str(request.data.get("name", ""))
                item.name = name
                item.save()
                response = {
                    "id": item.id,
                    "name": item.name,
                    "date_created": item.date_created,
                    "date_modified": item.date_modified,
                    "bucketlist_id": item.bucketlist_id
                }
                return make_response(jsonify(response)), 200

            elif request.method == "GET":
                # Fetch the specified bucketlist
                response = {
                    "id": item.id,
                    "name": item.name,
                    "date_created": item.date_created,
                    "date_modified": item.date_modified,
                    "bucketlist_id": item.bucketlist_id
                }
                return make_response(jsonify(response)), 200

            else:
                # delete the item using our delete method
                item.delete()
                return {"message": "item {} deleted".
                        format(item.id)}, 200

        # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
