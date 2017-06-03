from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(20))
    bucketlists = db.relationship(
        "BucketList", order_by="BucketList.id", cascade="all, delete-orphan",
        lazy="dynamic")

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        # check password against the hashed one to validate user
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        # save new or edited user
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"


class BucketList(db.Model):
    __tablename__ = "bucketlists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    date_modified = db.Column(db.DateTime, default=datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    bucketlist_items = db.relationship(
        "BucketListItem", order_by="BucketListItem.bucketlist_id",
        cascade="all, delete-orphan", lazy="dynamic")

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def save(self):
        # Save a new or edited bucketlist.
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        # get all the bucketlists for a given user
        return BucketList.query.filter_by(created_by=user_id)

    def delete(self):
        # Deletes a given bucketlist
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)


class BucketListItem(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    date_modified = db.Column(
        db.DateTime, default=datetime.now, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        BucketList.id), nullable=False)

    def __init__(self, name, bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id

    def save(self):
        # Save a new or edited bucketlist item
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(bucketlist_id):
        # get all the bucketlists items under a given bucketlist
        return BucketList.query.filter_by(bucketlist_id=bucketlist_id)

    def delete(self):
        # Deletes a given bucketlist item
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist_item: {}>".format(self.name)
