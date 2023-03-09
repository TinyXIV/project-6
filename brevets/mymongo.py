import os
import logging
from pymongo import MongoClient
import arrow
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.mydb

collection = db.lists


def brevets_insert(brevet_dist, start_time, checkpoints):
    """
    Inserts a new list into the database output, under the collection "lists".
    
    Inputs a title (string) and items (list of dictionaries)
    Returns the unique ID assigned to the document by mongo (primary key.)
    """


    
    output = collection.insert_one({
        "brevet_dist": brevet_dist,
        "start_time": start_time.format('YYYY-MM-DDTHH:mm'),
        "checkpoints": checkpoints
        })
    _id = output.inserted_id # this is how you obtain the primary key (_id) mongo assigns to your inserted document.
    return _id
    
    

def brevets_fetch():

    """
    Obtain the new brevet collection in database mydb/lists.
    Returns return start_time, brevet_dist, checkpoint
    """

    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    brevet = collection.find_one(sort=[('_id', -1)])
    start_time_str = brevet['start_time'].format('YYYY-MM-DDTHH:mm')

    return brevet['brevet_dist'], start_time_str, brevet['checkpoints']
