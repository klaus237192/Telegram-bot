from pymongo import MongoClient


def connect_to_database():
    # Connect to the MongoDB server
    try:
        client = MongoClient("mongodb://localhost:27017/")
        # Access a specific database and collection
        db = client["mydatabase"]
        return db["webhook_bot"]
    except Exception as e:
        print("database error")


def find_document_by_sessionid():
    # Connect to the database
    collection = connect_to_database()

    # Find the document that contains the sessionid
    return collection.find_one()


def insert_document(document):
    # Connect to the database
    collection = connect_to_database()
    collection.delete_many({})
    # Insert the document
    result = collection.insert_one(document)

    return result.inserted_id
