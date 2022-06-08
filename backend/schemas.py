'''
Validation
'''
from pydantic import BaseModel

class SQLQuery(BaseModel):
    SQL : str

class queryResult(BaseModel):
    data : list
    key : list