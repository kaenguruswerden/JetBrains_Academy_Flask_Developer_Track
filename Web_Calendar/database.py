from flask_restful import fields
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Events(db.Model):
    """The model class for an event entries in the database."""

    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)  # event id
    event = db.Column(db.String, nullable=False)  # event name/description
    date = db.Column(db.Date, nullable=False)  # event date, format yyyy-mm-dd


# Fields for the "Events" class, used for marshalling
event_resource_fields = {
    "id": fields.Integer,
    "event": fields.String,
    "date": fields.String
}
