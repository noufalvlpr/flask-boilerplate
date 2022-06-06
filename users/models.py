from sqlalchemy_serializer import SerializerMixin

from main import db


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    age = db.Column(db.Integer)
