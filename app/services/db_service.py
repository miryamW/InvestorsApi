from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

client = AsyncIOMotorClient('mongodb://localhost:27017')

db = client['UsersDubgetData']
users = db['users']
operations = db['operations']
