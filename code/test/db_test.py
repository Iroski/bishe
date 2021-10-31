import pymongo
import pprint

dbClient = pymongo.MongoClient("mongodb://localhost:27017/")

db = dbClient["bug_lib"]

itemCol = db["item"]
testData = {"name": "2", "numbers": [1, 2, 3, 4]}
itemCol.insert_one(testData)
findData = itemCol.find_one({"name": "2"})
pprint.pprint(findData)
