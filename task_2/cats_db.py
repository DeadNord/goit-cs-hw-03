# cat_database.py
from db_connector import DatabaseConnector

class CatDatabase:
    def __init__(self, collection_name):
        self.connector = DatabaseConnector()
        self.connector.connect()
        self.collection = self.connector.get_collection(collection_name)

    def insert_cat(self, name, age, features):
        cat = {"name": name, "age": age, "features": features}
        return self.collection.insert_one(cat).inserted_id

    def find_all_cats(self):
        return list(self.collection.find({}))

    def find_cat_by_name(self, name):
        return self.collection.find_one({"name": name})

    def update_cat_age(self, name, age):
        return self.collection.update_one({"name": name}, {"$set": {"age": age}})

    def add_cat_feature(self, name, feature):
        return self.collection.update_one({"name": name}, {"$push": {"features": feature}})

    def delete_cat_by_name(self, name):
        return self.collection.delete_one({"name": name})

    def delete_all_cats(self):
        return self.collection.delete_many({})
