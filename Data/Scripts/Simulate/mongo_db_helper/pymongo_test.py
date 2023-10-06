from bson import ObjectId
from pymongo import MongoClient


def create_connection():
    pass


def connect_collection():
    pass


def add_doc():
    pass


def update_doc():
    pass


def doc_structure(title, author, rate, contributors, url, comments):
    return {
        "title": title,
        "author": author,
        "rate": rate,
        "contributors": contributors,
        "comments": comments,
        "url": url
    }


def mongo_info(mongo_client, mongo_db):
    print(mongo_client.list_database_names())

    print(mongo_db.list_collection_names())


if __name__ == "__main__":
    # client connection
    client = MongoClient()
    # connect to db
    bookstore_db = client.bookstore

    mongo_info(client, bookstore_db)
    print("-" * 10)

    data = doc_structure("python test 0", "Pouria Parhami",
                         8,
                         ["Geeks", "Pouria", "HH"],
                         {"name": "bahare", "body": "Man Bishoram"},
                         {"name": "Bahare", "body": "Man bishouram!"}
                         )

    # connect to a collection of database
    books = bookstore_db.books
    # add one item to the collection
    # print("Insert one item.")
    # result = books.insert_one(data)
    # print(result)
    # print("-" * 10)
    #
    # print("Insert Multiple items.")

    data_one = doc_structure("python test one",
                             "Pouria Parhami",
                             9,
                             ["Gorje", "Pouria", "Kail"],
                             "www.test.come",
                             {"name": "Bahare", "body": "oh, khali khoob."})

    data_two = doc_structure("python test two",
                             "John Sti",
                             7,
                             ["Mike", "Pouria", "Helen"],
                             "www.test.come",
                             {"name": "Hooman", "body": "nice"})

    data_three = doc_structure("python test three",
                               "Pouria Parhami",
                               5,
                               ["Helen", "Pouria", "Dave"],
                               "www.test.come",
                               {"name": "Arghavan", "body": "wow! very good."})
    #
    # result = books.insert_many([data_one, data_two, data_three])
    # print(result)
    # print("-" * 10)

    print("find item in collection")
    result = books.find_one()
    print(result)

    print("-" * 10)
    print("find specific one item")
    result = books.find_one({"author": "John Sti"})  # case sensitive
    print(result)

    print("-" * 10)
    print("find one item by id")
    result = books.find_one({"_id": ObjectId("651d04e4279c272f2c5fcb72")})
    print(result)

    print("-" * 10)
    print("find some items")
    results = books.find({"author": "Pouria Parhami"})
    for result in results:
        print(result)

    print("-" * 10)
    print("count documents")
    print("count all documents")
    result = books.count_documents({})
    print(result)

    print("-" * 10)
    print("count specific documents")
    result = books.count_documents({"author": "Pouria Parhami"})
    print(result)

    print("-" * 10)
    print("find rate less than")
    results = books.find({"rate": {"$lt": 7}})
    for result in results:
        print(result)

    print("-" * 10)
    print("find grater than and sort")
    results = books.find({"rate": {"$gt": 6}}).sort("name")
    for result in results:
        print(result)

    # TODO create update
    print("-" * 10)
    print("update an item")
    result = books.update_one({})

    print("-" * 10)
    print("remove one item")
    result = books.remove_onw({"_id": ObjectId("651d1037dfd64128cb31e53a")})
