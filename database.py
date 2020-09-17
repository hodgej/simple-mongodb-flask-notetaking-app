import pymongo
from pymongo import MongoClient



def init_database(): #add functionality for more databases later
    print("didit")
    client = MongoClient('')
    db = client.notes
    collection = db.biology


def search_topic(topic, query):
    client = MongoClient('')
    db = client.notes
    collection = db[topic]
    print("query")
    print(query)
    found = collection.find_one({"subtopic": {"$regex": query[0], "$options": 'i'}}, {'_id':0})
    if list(found) == []:
        return "no_result"
    return found


def add_notes(classroom, data):

    class_collection = classroom
    client = MongoClient(
        'mongodb+srv://user:27332Jack!@cluster0.yhrtk.mongodb.net/<dbname>?retryWrites=true&w=majority')
    db = client.notes
    collection = db[class_collection]
    topic = data["topic"] #named subtopic in db
    data.pop("topic")
    collection.insert_one({"subtopic":topic})
    for i in data:
        collection.update_one(
            {"subtopic": topic},
            {"$addToSet": {str(i): data[i]}}
        )


