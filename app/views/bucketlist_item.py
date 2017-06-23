# /app/views/bucketlist_item.py
from flask.views import MethodView
from flask import request, jsonify, abort, make_response

import decorator
from app.models import BucketList, BucketListItem
from . import bucketlist_item_blueprint


class BucketListItemView(MethodView):

    @decorator.login_required
    def post(self, id, user_id):
        bucketlist = BucketList.query.filter_by(
            id=id, created_by=user_id).first()

        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        name = request.data.get("name", "").strip()
        if name:
            existing = BucketListItem.query.filter_by(name=name,
                                                      bucketlist_id=id).first()
            if existing:
                response = {"message": "Item exists"}
                return make_response(jsonify(response)), 205

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


class BucketListItemManipulationView(MethodView):

    @decorator.login_required
    def put(self, id, item_id, user_id):
        bucketlist = BucketList.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        item = BucketListItem.query.filter_by(id=item_id).first()

        if not item:
            # Raise an HTTPException
            abort(404)

        # Update bucketlist with new name
        name = request.data.get("name", "").strip()
        if name:
            existing = BucketListItem.query.filter_by(name=name,
                                                      bucketlist_id=id).first()
            if existing:
                response = {"message": "Name exists, enter another"}
                return make_response(jsonify(response)), 409

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

        response = {"message": "Enter a Valid Name"}
        return make_response(jsonify(response)), 400

    @decorator.login_required
    def get(self, id, item_id, user_id):
        # Fetch the specified bucketlist
        bucketlist = BucketList.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        item = BucketListItem.query.filter_by(id=item_id).first()

        if not item:
            # Raise an HTTPException
            abort(404)

        response = {
            "id": item.id,
            "name": item.name,
            "date_created": item.date_created,
            "date_modified": item.date_modified,
            "bucketlist_id": item.bucketlist_id
        }
        return make_response(jsonify(response)), 200

    @decorator.login_required
    def delete(self, id, item_id, user_id):
        bucketlist = BucketList.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        item = BucketListItem.query.filter_by(id=item_id).first()
        if not item:
            # Raise an HTTPException
            abort(404)

        # delete the item using delete method
        item.delete()
        return {"message": "item {} deleted".
                format(item.id)}, 200


# API resource
bucketlist_item_view = BucketListItemView.as_view("bucketlist_item_view")
item_manipulation_view = BucketListItemManipulationView.as_view(
    "item_manipulation_view")

# Rule for bucketlist item with blueprint
bucketlist_item_blueprint.add_url_rule("/bucketlists/<int:id>/items/",
                                       view_func=bucketlist_item_view,
                                       methods=["POST"])
bucketlist_item_blueprint.add_url_rule(
    "/bucketlists/<int:id>/items/<int:item_id>/",
    view_func=item_manipulation_view,
    methods=["PUT", "GET", "DELETE"])
