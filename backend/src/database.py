from pymongo import MongoClient

url = "mongodb://localhost:27017/summit-series-db"

client = MongoClient(url)
db = client["summit-series-db"]
