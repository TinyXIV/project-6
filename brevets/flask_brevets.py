"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
from pymongo import MongoClient
import mymongo

#Use these functions^^

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

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
    km = request.args.get('km', 999, type=float)
    distance = request.args.get('distance', type=int)
    start_time = arrow.get(request.args.get('start_time', '', type=str))

    app.logger.debug("km={}, distance={}, start_time={}".format(km, distance, start_time))
    app.logger.debug("request.args: {}".format(request.args))

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
    status = None
    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can do this:
        distance = input_json["distance"] # Should be a string
        start = input_json["start"]
        items = input_json["items"] # Should be a list of dictionaries
  
        status = mymongo.brevets_insert(distance, start, items)
        result={
            "message": "Inserted!", 
            "status":1, # This is defined by you. You just read this value in your javascript.
            "mongo_id": str(status)
            }
        
        return flask.jsonify(result=result)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        result={
            "message": "Oh no! Server error!",
            "status": 0, # This is defined by you. You just read this value in your javascript.
            "mongo_id": str(status)
            }
        return flask.jsonify(result = result)


@app.route("/fetch_brevet")
def fetch_brevet():
    """
    /fetch : fetches the newest to-do list from the database.
    Accepts GET requests ONLY!
    JSON interface: gets JSON, responds with JSON
    """
    try:

        distance, start, items = mymongo.brevets_fetch()
        result ={
            "info": {"distance": str(distance), "start": str(start), "items": items},
            "status": 1,
            "message": "Successfully fetched the newest brevet"
            }

        return flask.jsonify(result= result)
    except:
        result ={"info": {"distance": None, "start": None, "items": []}, 
        "status": 0, 
        "message": "Something went wrong, couldn't fetch any lists!"}
        return flask.jsonify(result= result)
#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
