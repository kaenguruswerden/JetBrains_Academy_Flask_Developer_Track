from datetime import date

from flask_restful import Resource, marshal_with
from flask import abort

from database import db, Events, event_resource_fields
from request_parser import event_parser, interval_parser


class TodaysEventsResource(Resource):
    @staticmethod
    @marshal_with(event_resource_fields)
    def get():
        # print("TodaysEvents")
        todays_events = Events.query.filter(Events.date == date.today()).all()
        return todays_events


class AllEventsResource(Resource):
    @staticmethod
    def post():
        args = event_parser.parse_args()
        event = Events(event=args["event"], date=args["date"].date())
        db.session.add(event)
        db.session.commit()
        response = {
            "message": "The event has been added!",
            "event": args["event"],
            "date": str(args["date"].date())
        }
        return response, 200

    @staticmethod
    @marshal_with(event_resource_fields)
    def get():
        # print("AllEvents")
        args = interval_parser.parse_args()
        if not args["start_time"] and not args["end_time"]:
            events = Events.query.all()
        elif args["start_time"] and not args["end_time"] or not args["start_time"] and args["end_time"]:
            abort(404, "Incorrect time interval")
            return  # not necessary, abort should be enough, just to prevent PyCharm warning
        else:
            events = Events.query.filter(Events.date.between(args["start_time"].date(), args["end_time"].date())).all()
        return events


class EventByID(Resource):
    @staticmethod
    @marshal_with(event_resource_fields)
    def get(event_id):
        # print("ByID")
        event = Events.query.filter(Events.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        return event

    @staticmethod
    def delete(event_id):
        event = Events.query.filter(Events.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        return {"message": "The event has been deleted!"}, 200
