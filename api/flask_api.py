"""
Brevets RESTful API
"""
import logging
import os
from flask import Flask
from flask_restful import Api
from mongoengine import connect
# You need to implement two resources: Brevet and Brevets.

from resources.brevet import BrevetResource
from resources.brevets import BrevetsResource


# Connect MongoEngine to mongodb
connect(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017/brevetsdb")

# Start Flask app and Api here:
app = Flask(__name__)
api = Api(app)

# Bind resources to paths here:
# api.add_resource(...)
api.add_resource(BrevetResource, '/api/brevet/<_id>')
api.add_resource(BrevetsResource, '/api/brevets')

if __name__ == "__main__":
    # Run flask app normally
    # Read DEBUG and PORT from environment variables.
    app.run(debug=os.environ['DEBUG'], port= os.environ['PORT'], host='0.0.0.0')
