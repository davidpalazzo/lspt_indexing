import pprint

import pymongo
from pymongo import MongoClient

# class IndexingDB:
#
#     def put(self, word, mapping):


def test():
    client = MongoClient('localhost', 27017)
    db = client['test_storage']

    post = {
        "Word": "test word",

        "List1": {
            "docs": [1, 2, 3]
        },

        "List2": {
            "word_freq": [
                {
                    "doc": 1,
                    "freq": 2
                },

                {
                    "doc": 2,
                    "freq": 1
                },

                {
                    "doc": 3,
                    "freq": 3
                }
            ]
        },

        "List3": {
            "word_pos": [
                {
                    "doc": 1,
                    "pos": [14, 56]
                },

                {
                    "doc": 2,
                    "pos": [20]
                },

                {
                    "doc": 3,
                    "pos": [17, 40, 78]
                }
            ]
        }
    }

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    # print(post_id)
    #
    # obj = posts.find_one({"Word": "test word"})
    # print(obj['List2']["word_freq"])
    # pprint.pprint(obj)

    print(posts.count_documents({}))


if __name__ == "__main__":
    test()
    client = MongoClient('localhost', 27017)
    db = client['test_storage']

    # # dblist = client.list_database_names()
    # # for db in dblist:
    # #     print(db)
    #

    # db.posts.create_index([("Word", pymongo.ASCENDING)], unique=True)
    #
    # posts = db.posts
    # for post in posts.find():
    #     print(post)