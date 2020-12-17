from dotenv import load_dotenv
import os
from pydal import DAL, Field

load_dotenv()
connection_string = os.getenv('CONNECTION_STRING')

def getDB(): 
    DB = DAL(connection_string)
    DB.define_table('config', Field("key", unique=True), Field('guild'),Field('value'), redefine = True)    
    return DB

