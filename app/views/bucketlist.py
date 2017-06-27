# /app/views/bucketlist.py
from flask.views import MethodView
from flask import request, jsonify, abort, make_response

from decorator import login_required
from app.models import BucketList, BucketListItem
from . import bucketlist_blueprint


class BucketListView(MethodView):
    decorators = [login_required]

    def post(self, user_id):
        name = request.data.get("name", "").strip()
        if name:
            existing = BucketList.query.filter_by(name=name,
                                                  created_by=user_id).first()
            if existing:
                response = {"message": "Bucketlist exists"}
                return make_response(jsonify(response)), 409

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

        response = {"message": "Bucketlist can not be blank name"}
        return make_response(jsonify(response)), 400

    def get(self, user_id):
        # GET all bucketlist by user
        limit = request.args.get("limit", 20)
        page = request.args.get("page", 1)
        q = request.args.get("q", None)
        limit = 100 if int(limit) > 100 else int(limit)

        if q:
            bucketlists = BucketList.query.filter(
                BucketList.name.ilike("%" + q + "%")).filter_by(
                created_by=user_id)
        else:
            bucketlists = BucketList.query.filter_by(
                created_by=user_id)

        bucketlists_pagination = bucketlists.paginate(int(page),
                                                      int(limit), False)
        results = []
        for bucketlist in bucketlists_pagination.items:
            details = {
                "id": bucketlist.id,
                "name": bucketlist.name,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified,
                "created_by": bucketlist.created_by
            }
            results.append(details)
        return make_response(jsonify(results)), 200


class BucketListManipulationView(MethodView):

    decorators = [login_required]

    def put(self, id, user_id):
        # filter bucketlist with id and user_id
        bucketlist = BucketList.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        # Update bucketlist with new name
        name = request.data.get("name", "").strip()
        if name:
            existing = BucketList.query.filter_by(
                name=name, created_by=user_id).first()

            if existing:
                response = {"message": "Name exists, enter another"}
                return make_response(jsonify(response)), 409

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

        response = {"message": "Enter a Valid Name"}
        return make_response(jsonify(response)), 400

    def get(self, id, user_id):
        # Fetch the specified bucketlist
        bucketlist = BucketList.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
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

    def delete(self, id, user_id):
        bucketlist = BucketList.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        # delete the bucketlist using delete method
        bucketlist.delete()
        return {"message": "bucketlist {} deleted".
                format(bucketlist.id)}, 200


# API resource
bucketlist_view = BucketListView.as_view("bucketlist_view")
manipulation_view = BucketListManipulationView.as_view("manipulation_view")

# Rule for bucketlist with blueprint
bucketlist_blueprint.add_url_rule("/bucketlists/", view_func=bucketlist_view,
                                  methods=["POST", "GET"])
bucketlist_blueprint.add_url_rule(
    "/bucketlists/<int:id>/", view_func=manipulation_view,
    methods=["PUT", "GET", "DELETE"])
