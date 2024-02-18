from pymongo import MongoClient
from datetime import datetime
from settings import MONGODB_URI

class Database:
    client = None

    def __init__(self, database_name, collection_name):
        self.database_name = database_name
        self.collection_name = collection_name
        if self.client is None:
            self.connect_to_db()
        
        
    def connect_to_db(self):
        self.client = MongoClient(MONGODB_URI)

    def close_connection(self):
        if self.client:
            self.client.close()


if __name__ == "__main__":
    Database(database_name="", collection_name="histo-portfolio")