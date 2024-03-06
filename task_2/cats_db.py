from db_connector import DatabaseConnector
from pymongo.errors import PyMongoError


class CatDatabase:
    def __init__(self, collection_name):
        self.connector = DatabaseConnector()
        self.connector.connect()
        self.collection = self.connector.get_collection(collection_name)

    def insert_cat(self, name, age, features):
        try:
            cat = {"name": name, "age": age, "features": features}
            return self.collection.insert_one(cat).inserted_id
        except PyMongoError as e:
            print(f"An error occurred while inserting the cat: {e}")

    def find_all_cats(self):
        try:
            return list(self.collection.find({}))
        except PyMongoError as e:
            print(f"An error occurred while finding all cats: {e}")

    def find_cat_by_name(self, name):
        try:
            return self.collection.find_one({"name": name})
        except PyMongoError as e:
            print(f"An error occurred while finding the cat by name: {e}")

    def update_cat_age(self, name, age):
        try:
            return self.collection.update_one({"name": name}, {"$set": {"age": age}})
        except PyMongoError as e:
            print(f"An error occurred while updating the cat's age: {e}")

    def add_cat_feature(self, name, feature):
        try:
            return self.collection.update_one(
                {"name": name}, {"$push": {"features": feature}}
            )
        except PyMongoError as e:
            print(f"An error occurred while adding a feature to the cat: {e}")

    def delete_cat_by_name(self, name):
        try:
            return self.collection.delete_one({"name": name})
        except PyMongoError as e:
            print(f"An error occurred while deleting the cat: {e}")

    def delete_all_cats(self):
        try:
            return self.collection.delete_many({})
        except PyMongoError as e:
            print(f"An error occurred while deleting all cats: {e}")
