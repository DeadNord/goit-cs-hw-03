from pymongo import MongoClient
from dotenv import dotenv_values


class DatabaseConnector:
    """Class responsible for managing database connections."""

    def __init__(self):
        config = dotenv_values(".env")  # Directly using dotenv_values to load config
        self.uri = config["MONGO_URI"]
        self.db_name = config["MONGO_DB_NAME"]
        self.client = None
        self.db = None

    def connect(self):
        """Establish a database connection."""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            print("Database connection successful.")
        except Exception as e:
            print(f"Failed to connect to the database: {e}")

    def get_collection(self, collection_name):
        """Get a collection from the database."""
        if self.db is not None:
            return self.db[collection_name]
        else:
            print("Database is not connected. Please call connect() method first.")
            return None
