# /app/views/bucketlist_item.py
from flask import request, jsonify, abort, make_response

import decorator
from app.models import BucketList, BucketListItem
from . import bucketlist_item_blueprint as app


@app.route("/bucketlists/<int:id>/items/", methods=["POST"])
@decorator.login_required
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
@decorator.login_required
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
            if name:
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
            else:
                response = {"message": "Enter a Valid Name"}
                return make_response(jsonify(response)), 400

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
            # delete the item using delete method
            item.delete()
            return {"message": "item {} deleted".
                    format(item.id)}, 200
