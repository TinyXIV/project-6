from mongoengine.queryset.manager import QuerySetManager


"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevets
from mongoengine.errors import DoesNotExist



class BrevetResource(Resource):

    def get(self, _id):
        try:
            brevet = Brevets.objects.get(id=_id).to_json()
            return Response(brevet, mimetype="application/json", status=200)
            
        except DoesNotExist:
            return f"Brevet id {_id} cannot be found.", 404


    def put(self, _id):
        try:
            data = request.json
            brevet = Brevets.objects.get(id=_id)
            brevet.update(**data)
            brevet.reload()
            return '', 200
            
        except DoesNotExist:
            return f"Brevet id {_id} cannot not be found.", 404  


    def delete(self, _id):
        try:
            Brevets.objects.get(id=_id).delete()
            return '', 200
            
        except DoesNotExist:
            return f"Brevet id {_id} cannot be found.", 404
        



# MongoEngine queries:
# Brevet.objects() : similar to find_all. Returns a MongoEngine query
# Brevet(...).save() : creates new brevet
# Brevet.objects.get(id=...) : similar to find_one

# Two options when returning responses:
#
# return Response(json_object, mimetype="application/json", status=200)
# return python_dict, 200
#
# Why would you need both?
# Flask-RESTful's default behavior:
# Return python dictionary and status code,
# it will serialize the dictionary as a JSON.
#
# MongoEngine's objects() has a .to_json() but not a .to_dict(),
# So when you're returning a brevet / brevets, you need to convert
# it from a MongoEngine query object to a JSON and send back the JSON
# directly instead of letting Flask-RESTful attempt to convert it to a
# JSON for you.
