#Code to validate data flowing through the API

from pydantic import BaseModel,validator, EmailStr, Extra
from datetime import date
from enum import Enum
# from marshmallow import Schema, fields, validate, ValidationError
import configparser



#----------------------
#---Configure Schema---
#----------------------
def get_config(path = 'deletion_app.cfg'):
    config = configparser.ConfigParser()
    config.read(path)
    return config

def get_config_data_specs():
    return get_config()['DATA_SPECS']

#-------------------
#---Data Schemas:---
#-------------------
#Making enumerated class dynamically
causes_dict = {cause:cause for cause in get_config_data_specs()['request_causes'].split(",")}
RequestCauses = Enum("RequestCauses",causes_dict)

class NewRequest(BaseModel):
    class Config:
        extra = Extra.forbid
    email: EmailStr
    request_cause: RequestCauses

class NewRequestList(BaseModel):
    requests: list[NewRequest]

#----------------
class EditPendingRequest(BaseModel):
    class Config:
        extra = Extra.forbid
    request_cause: RequestCauses = None
    rejected: bool = None

#----------------
class GetFinishedByDate(BaseModel):
    class Config:
        extra = Extra.forbid
    startDate: str = None
    endDate: str = None

    @validator('startDate','endDate')
    def correct_time_format(cls,value):
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError("Incorrect date format. Please use YYYY-MM-DD")


#---------------------
#---Header Schemas:---
#---------------------
class AuthenticationHeaderSchema():
    #class to be implemented once we have authentication set up
    #Something maybe like "apiKey:xxx-xxx-xxx"
    pass