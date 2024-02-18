from pymongo import MongoClient
from datetime import datetime
from settings import MONGODB_URI
from database.database import Database

class PortfolioDB(Database):
    def __init__(self, collection_name):
        super().__init__(collection_name=collection_name)

    def connect_to_db(self):
        self.client = MongoClient(MONGODB_URI)

    def close_connection(self):
        if self.client:
            self.client.close()

    def insert_portfolio_data(self, exchange_name, portfolio_data):
        try:
            db = self.client[self.database_name]
            collection = db[self.collection_name]

            # Insert portfolio data to MongoDB
            collection.insert_one({
                "exchange": exchange_name,
                "timestamp": datetime.now(),
                "portfolio": portfolio_data
            })

            print("Portfolio data saved to MongoDB successfully.")
        except Exception as e:
            print(f"Error saving portfolio data to MongoDB: {e}")

    def query_portfolio_data(self, exchange_name, start_date=None, end_date=None):
        try:
            db = self.client[self.database_name]
            collection = db[self.collection_name]

            query = {"exchange": exchange_name}
            if start_date and end_date:
                query["timestamp"] = {"$gte": start_date, "$lte": end_date}

            # Query portfolio data from MongoDB
            result = list(collection.find(query))

            return result
        except Exception as e:
            print(f"Error querying portfolio data from MongoDB: {e}")
            return None