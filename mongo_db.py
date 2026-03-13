from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB

def connect_mongo():
    """Connexion à la base entertainment, collection films"""
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db["films"]