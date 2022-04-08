from flask_restful import reqparse, inputs


parser = reqparse.RequestParser()
parser.add_argument(
    "date",
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True,
    location=["args", "form"]
)

parser.add_argument(
    "event",
    type=str,
    help="The event name is required!",
    required=True,
    location=["args", "form"]
)

interval_parser = reqparse.RequestParser()
interval_parser.add_argument(
    "start_time",
    type=inputs.date,
    help="The start time with the correct format is required! The correct format is YYYY-MM-DD!",
    required=False,
    location=["args", "form"]
)

interval_parser.add_argument(
    "end_time",
    type=inputs.date,
    help="The end time with the correct format is required! The correct format is YYYY-MM-DD!",
    required=False,
    location=["args", "form"]
)
