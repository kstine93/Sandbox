#Example Docker App using this resource:
#https://docs.docker.com/language/python/build-images/

from typing import Type

from fastapi import FastAPI, Response
from pydantic import BaseModel, Extra
#from flask import Flask, render_template, request

from databaseConnection import DatabaseConnection

from marshmallow import ValidationError
from api.validation import *

#----------------
db = DatabaseConnection()

#----------------
app = FastAPI()
base_url = '/api/v1'
requests_url = base_url + '/requests'

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
def edit_pending_requests(id:int, body: EditPendingRequest):

    #Filtering out default 'None' values
    values = {key:val for key,val in body.dict().items() if val is not None}
    if values:
        #Updating Data
        try:
            db.edit_pending_by_id(id,**values)
            return Response(f"Attributes changed for id {id}\n", 200)
        except Exception as err:
            return Response(str(err), 400)

    else:
        return Response("Error: No attributes provided in JSON request body\n", 422)

# #--------------
# #---FINISHED---
# #--------------
# @app.route(requests_url + '/finished', methods=['POST'])
# def read_finished_requests():

#     #If any data attached:
#     if request.data:

#         #Validating Payload
#         try:
#             data = GetFinishedByDate(many=False).load(data=request.json)
#         except ValidationError as err:
#             return err.messages_dict, 400

#         try:
#             return db.get_finished_by_date(data['startDate'],data['endDate']), 200
#         except Exception as err:
#             return str(err), 400

#     else:
#         return db.get_finished(), 200