from dotenv import load_dotenv
import pymongo
import os
import csv
from bson.objectid import ObjectId
load_dotenv()



client = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('MONGO_DB')]
result=db.team.aggregate([
    {"$skip": 12},
    {"$limit": 1},
])
totalItems = db.team.count_documents()
print(totalItems)
print(list(result))
