import os
import logging
import arrow
import requests    # The library we use to send requests to the API
# Not to be confused with flask.request.


API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api"


def brevets_insert(brevet_dist, start_time, checkpoints):
    """
    Inserts a new list into the database output, under the collection "lists".
    
    Inputs a title (string) and items (list of dictionaries)
    Returns the unique ID assigned to the document by mongo (primary key.)
    """
    formatted_start_time = start_time.format('YYYY-MM-DDTHH:mm')

    formatted_checkpoints = []


    for checkpoint in checkpoints:
        formatted_checkpoint = {
            "distance": checkpoint["distance"],
            "open_time": checkpoint["open_time"].format('YYYY-MM-DDTHH:mm'),
            "close_time": checkpoint["close_time"].format('YYYY-MM-DDTHH:mm')
        }
        formatted_checkpoints.append(formatted_checkpoint)

    data = {
        "brevet_dist": brevet_dist,
        "start_time": formatted_start_time,
        "checkpoints": formatted_checkpoints
    }


    response = requests.post(f"{API_URL}/brevets", json=data)
    return response.json()["_id"]


    

def brevets_fetch():

    """
    Obtain the new brevet collection in database mydb/lists.
    Returns return start_time, brevet_dist, checkpoint
    """

    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.
    output = requests.get(f"{API_URL}/brevets").json()
    brevet = output[-1]
    

    
    return brevet["brevet_dist"], brevet["start_time"], brevet["checkpoints"]
    
