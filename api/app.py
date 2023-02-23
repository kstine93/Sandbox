#Example Docker App using this resource:
#https://docs.docker.com/language/python/build-images/

from fastapi import FastAPI, Response
#from flask import Flask, render_template, request

from databaseConnection import DatabaseConnection

#----------------
db = DatabaseConnection()

from validation import *

#----------------
app = FastAPI()
base_url = '/api/v1'
requests_url = base_url + '/requests'

#----------------
def filterNoneValsFromDict(obj: dict) -> dict:
    '''Removes items from dict where value == None
    
    Parameter
    ---------
    obj: dict
        dictionary in need of filtering.

    Returns
    -------
    dict
        dictionary after filtering.
    '''
    return {key:val for key,val in obj.items() if val is not None}

#----------------
def stringsFromEnumDict(obj: dict) -> dict:
    '''If any values of given dict are instances of an Enum class
    get just the value- not the entire class. Doesn't change other values.

    Parameter
    ---------
    obj: dict
        dictionary which might have classes as values

    Returns
    -------
    dict
        dictionary with only values - no classes.
    '''
    return {key:(val.value if isinstance(val,Enum) else val) for key,val in obj.items()}

#---------
#---NEW---
#---------
@app.post(requests_url + '/new')
async def add_requests(body: NewRequestList):

    #Adding data to database
    for item in body.requests:
        db.add_new_by_email(email=item.email,cause=item.request_cause.value)

    return Response("New requests successfully added.\n",200)

#-------------
#---PENDING---
#-------------
@app.get(requests_url + '/pending')
async def read_pending_requests():
    #TODO: Implement validation on returned data (make another pydantic class)
    return db.get_pending()

#--------------
@app.post(requests_url + "/pending/{id}")
async def edit_pending_requests(id:int, body: EditPendingRequest | None = None):

    if not body:
        return Response("Warning: empty request body - please provide attributes to change.", 422)
    
    #Filtering out default 'None' values
    values = filterNoneValsFromDict(body.dict())
    #Converting Enums to strings:
    values = stringsFromEnumDict(values)
    if values:
        #Updating Data
        try:
            db.edit_pending_by_id(id,**values)
            return Response(f"Attributes changed for id {id}\n", 200)
        except Exception as err:
            return Response(str(err), 400)

    else:
        return Response("Warning: No attributes provided in JSON request body. No changes made.\n", 422)

#--------------
#---FINISHED---
#--------------

@app.post(requests_url + '/finished')
async def read_finished_requests(body: GetFinishedByDate | None = None):
    
    if not body:
        return db.get_finished()
    
    #Filtering out default 'None' values
    values = filterNoneValsFromDict(body.dict())
    if values:
        #retrieving data based on date criteria
        try:
            return Response(db.get_finished_by_date(**values), 200)
        except Exception as err:
            return Response(str(err), 400)

    else:
        return db.get_finished()