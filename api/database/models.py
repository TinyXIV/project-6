from mongoengine import Document, StringField, FloatField, DateTimeField, ListField, EmbeddedDocumentField, EmbeddedDocument
from mongoengine.queryset.manager import QuerySetManager

class Checkpoint(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
        distance: MongoEngine float field, required, (checkpoint distance in kilometers),
		location: MongoEngine string field, optional, (checkpoint location name),
		open_time: MongoEngine datetime field, required, (checkpoint opening time),
		close_time: MongoEngine datetime field, required, (checkpoint closing time).
    """
    distance = FloatField(required=True)      # checkpoint distance in kilometers
    location = StringField()                 # checkpoint location name
    open_time = DateTimeField(required=True)  # checkpoint opening time
    close_time = DateTimeField(required=True) # checkpoint closing time


class MyBrevet(Document):
    """
    A MongoEngine document containing:
		length: MongoEngine float field, required
		start_time: MongoEngine datetime field, required
		checkpoints: MongoEngine list field of Checkpoints, required
    """
    brevet_dist = FloatField(required=True)        # brevet distance in kilometers
    start_time = DateTimeField(required=True) # brevet start time
    checkpoints = ListField(EmbeddedDocumentField(Checkpoint), required=True) # checkpoints
    objects = QuerySetManager() 
