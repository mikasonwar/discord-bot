from dotenv import load_dotenv
import os
from pydal import DAL, Field

load_dotenv()
connection_string = os.getenv('CONNECTION_STRING', 'sqlite://storage.db')

def getDB(): 
    DB = DAL(connection_string)
    DB.define_table('config', Field("key", unique=True), Field('guild'),Field('value'), redefine = True)
    DB.define_table('presence', Field('value'), redefine = True)
    DB.define_table('birthdays', Field('user_id', unique=True), Field('birthday'),redefine = True)
    return DB

