from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
client = AsyncIOMotorClient('mongodb://localhost:27017')
synchronise_client = MongoClient('mongodb://localhost:27017')

db = client['UsersDubgetData']
users = db['users']
operations = db['operations']
synchronise_db = synchronise_client['UsersDubgetData']
synchronise_users = synchronise_db['users']
synchronise_operations = synchronise_db['operations']

