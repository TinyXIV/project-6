"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""
import os
import flask
import myapi
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations






#Use these functions^^

import logging

###
# Globals
###
app = flask.Flask(__name__)


###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = flask.request.args.get('km', 999, type=float)
    distance = flask.request.args.get('distance', type=int)
    start_time = arrow.get(flask.request.args.get('start_time', '', type=str))

    app.logger.debug("km={}, distance={}, start_time={}".format(km, distance, start_time))
    app.logger.debug("flask.request.args: {}".format(flask.request.args))

    open_time = acp_times.open_time(km, distance, start_time).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, distance, start_time).format('YYYY-MM-DDTHH:mm')
    #Old Code
    #(km, distance, arrow.now().isoformat).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

#Lab Tips:
#Two more app.routes for fetch and insert functions
#Get information same I got km above, from what the javascript gives them
#Call the functions within the app route 
@app.route("/insert_brevet", methods=["POST"])
def insert_brevet():
    """
    /insert_brevet : inserts race info list into the database.
    Accepts POST requests ONLY!
    JSON interface: gets JSON, responds with JSON
    """
    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = flask.request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can do this:
        brevet_dist = float(input_json["brevet_dist"])
        start_time = arrow.get(input_json["start_time"])
        checkpoints = input_json["checkpoints"] # Should be a list of dictionaries
        
        app.logger.debug("dist={}, start_time={}, checkpoints={}".format(brevet_dist, start_time, checkpoints))
       # Insert the brevet into the database using the myapi.brevets_insert function
        _id = myapi.brevets_insert(brevet_dist, start_time, checkpoints)
        
        result ={
            "message": "Successfully inserted the brevet.",
            "status": 1,
            "_id": _id
        }
        
        # Return the inserted brevet object as JSON
        return flask.jsonify(result = result), 200
    except (ValueError, KeyError):
        return flask.jsonify(error="Invalid input data"), 400
        


@app.route("/fetch_brevet", methods=["GET"])
def fetch_brevet():
    """
    /fetch : fetches the newest to-do list from the database.
    Accepts GET requests ONLY!
    JSON interface: gets JSON, responds with JSON
    """
    try:

        # Fetch the newest brevet from the database using the myapi.brevets_fetch function
        brevet_dist, start_time, checkpoints = myapi.brevets_fetch()
        

        result ={
            "brevet": {"brevet_dist": brevet_dist, "start_time": start_time, "items": checkpoints},
            "status": 1,
            "message": "Successfully fetched the brevets list."
        }

        return flask.jsonify(result= result)
    except:
        result = {
            "brevets": [],
            "status": 0,
            "message": "Brevets list not found."
        }
        return flask.jsonify(result=result)
#############

app.debug = os.environ["DEBUG"]
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.run(port = os.environ["PORT"], host="0.0.0.0")
