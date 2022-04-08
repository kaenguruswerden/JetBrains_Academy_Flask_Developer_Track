import sys

from flask import Flask
from flask_restful import Api

from database import db
from request_resources import TodaysEventsResource, AllEventsResource, EventByID


# Set up the main app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set up the database
db.init_app(app)
db.create_all(app=app)

# Set up the API for the app
api = Api(app)

api.add_resource(TodaysEventsResource, "/event/today")
api.add_resource(AllEventsResource, "/event")
api.add_resource(EventByID, "/event/<int:event_id>")

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(debug=True)
