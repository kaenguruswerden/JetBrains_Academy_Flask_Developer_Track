from flask_restful import fields
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Events(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)


event_resource_fields = {
    "id": fields.Integer,
    "event": fields.String,
    "date": fields.String
}
