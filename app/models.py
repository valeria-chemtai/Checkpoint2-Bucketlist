from app import db
from datetime import datetime, timedelta


class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(20))
    bucketlists = db.relationship(
        'Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")


class BucketList(db.Model):
    __tablename__ = "Bucketlists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    date_modified = db.Column(db.DateTime, default=datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))


class BucketListItem(db.Model):
    __tablename__ = "Items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    date_modified = db.Column(
        db.DateTime, default=datetime.now, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        "Bucketlists.id"), nullable=False)
