import pymongo
from bson import timestamp
from bson.son import SON
from bson.code import Code
from pymongo import MongoClient
import time

import pprint

PORT = 27017
HOST = "localhost"
DATABASE = "test_storage"
COLLECTION = "test-collection-4"
COLLECTION_MR = "test-map-reduce-4"

'''
New Design for Concurrent operation:
Apply incremental map-reduce mechanism for updating collection 1 to collection 2
Incremental apply time stamp for storing the update

Collection 1:
{
    "text": "my_word",
    "ts": "20190817xxxx"
    "documentId": 5da65f292f67f000015296c,
    "tf": 0.308,
    "idf": 2.996,
    "occurrences": [1, 4, 10, 13]    
}

Collection 2:
{
    "_id": "my_word",
    "value": {
        "ts": "20190817xxxx",   # the last time update 
        "documents": {
            "5da65f292f67f000015296c":
            {
                "tf": 0.308,
                "idf": 2.996,
                "occurrences": [1, 4, 10, 13]
            },

            "2kn3sdf0012nh19287560d":
            { 
                "tf": 0.416,
                "idf": 3.0,
                "occurrences": [1, 4]
            }
        }
    }
}
'''


class DataLayer:
    def __init__(self):
        client = MongoClient(HOST, PORT)
        self.collection = client[DATABASE][COLLECTION]
        self.mr_collection = client[DATABASE][COLLECTION_MR]

        success = self.collection.create_index([("text", pymongo.ASCENDING),
                                                ("documentId", pymongo.ASCENDING)], unique=True)
        if success:
            print("create index on collection {} success".format(COLLECTION))

    """
    input: example_contents = 
    [
        {
            "text": "Test2",
            "documentId": "5da65f292f67f000015296c",
            "document": 
            {
                "tf": 0.301,
                "idf": 3.912,
                "occurrences": [1, 100]
            }
        },

        {
             "text": "Lambda",
             "documentId": "2kn3sdf0012nh19287560d",
             "document": 
             {
                "tf": 0.416,
                "idf": 3.0,
                "occurrences": [1, 4]
             }
        }
    ]
    """

    def put(self, contents):
        last_update = time.time()
        insert_ids = list()
        for content in contents:
            self.collection.update_one(
                {"text": content["text"], "documentId": content["documentId"]},
                {"$set": {"ts": time.time(), "document": content["document"]}},
                upsert=True
            )
        dataLayer.mr_aggregation(last_update)
        return insert_ids

    def mr_aggregation(self, last_update):
        mapper = Code(
            '''
            function () {
                var key = this.text;
                var value = {"documents": {}}
                value["documents"][this.documentId] = this.document;
                value["documents"][this.documentId]["ts"] = this.ts;
                emit(key, value);
            }
            '''
        )

        reducer = Code(
            '''
            function (key, values) {
                var obj = {};
                obj["documents"] = {};
                
                function merge(documentId, document) {
                    if (documentId in obj["documents"] &&
                        obj["documents"][documentId]["ts"] > document["ts"]) {
                        return;
                    }
                    obj["documents"][documentId] = document;
                }
                
                for (var i = 0; i < values.length; i ++) {
                    var value = values[i];
                    for(let documentId in value["documents"]) {
                        merge(documentId, value["documents"][documentId])
                    }
                }
                return obj;
            }
            '''
        )

        return self.collection.map_reduce(mapper, reducer,
                                          out={"reduce": COLLECTION_MR},
                                          query={"ts": {"$gte": last_update}},
                                          )

    def get(self, collection, queries):
        # Currently just search text one by one,
        # Later can apply find to search for multiple result
        result_list = list()
        for query in queries:
            print("there are {} document with {}".format(collection.count_documents(query), query))
            ones = collection.find(query)
            for one in ones:
                result_list.append(one)
        return result_list

    def remove_text(self, collection, query):
        success = collection.delete_many(query)
        print(success)


if __name__ == "__main__":
    example_contents = [
        {
            "text": "Lambda",
            "documentId": "5da65f292f67f000015296c",
            "document":
                {
                    "tf": 0.301,
                    "idf": 3.912,
                    "occurrences": [12, 17, 20]
                }
        },

        {
            "text": "Lambda",
            "documentId": "2kn3sdf0012nh19287560d",
            "document":
                {
                    "tf": 0.416,
                    "idf": 3.0,
                    "occurrences": [1, 4, 5]
                }
        },

        {
            "text": "MyTest",
            "documentId": "good good study day day up",
            "document":
                {
                    "tf": 0.416,
                    "idf": 3.0,
                    "occurrences": [9, 99, 999]
                }
        },

        {
            "text": "Lambda",
            "documentId": "10010",
            "document":
                {
                    "tf": 0.301,
                    "idf": 3.912,
                    "occurrences": [12, 17, 20]
                }
        }
    ]

    dataLayer = DataLayer()
    # dataLayer.remove_text(dataLayer.collection, {})
    # dataLayer.remove_text(dataLayer.mr_collection, {})

    dataLayer.put(example_contents)

    results = dataLayer.get(dataLayer.collection, [{}])
    for result in results:
        pprint.pprint(result)

    print("-----------------------FROM QUERY--------------------------")
    results = dataLayer.get(dataLayer.mr_collection, [{}])
    for result in results:
        pprint.pprint(result)
