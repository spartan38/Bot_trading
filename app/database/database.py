from pymongo import MongoClient
from datetime import datetime
from settings import MONGODB_URI

class Database:
    client = None

    def __init__(self, collection_name):
        self.collection_name = collection_name
        if self.client is None:
            self.connect_to_db()
        
        
    def connect_to_db(self):
        self.client = MongoClient(MONGODB_URI).client

    def close_connection(self):
        if self.client:
            self.client.close()
