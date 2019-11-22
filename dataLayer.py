import pprint

import pymongo
from pymongo import MongoClient
from bson.son import SON
from bson.code import Code

# TODO: DataLayer is going to apply indexing mechanism in order to accelerate the queries
# TODO: upgrade from non-indexing to indexing key, removing duplicate if necessary
# TODO: consider to move the LRU to the data layer?

'''
Configuration of the data base, specified as constants.
if more privacy is required, this should be loaded from document,
and use authentication of accessing database
'''

PORT = 27017
HOST = "localhost"
DATABASE = "test_storage"
COLLECTION = "test-collection"


class DataLayer:

    def __init__(self):
        client = MongoClient(HOST, PORT)
        self.collection = client[DATABASE][COLLECTION]

        success = self.collection.create_index([('text', pymongo.ASCENDING)], unique=False)
        if success:
            print("create index on [text] success")

    '''
    Description: put the list of contents into the database.
    Parameters: “contents” is a list of word objects defined by our database schema in ‘Detailed Sub-Component Design’. 
                Each is associated with a map of documents, with document ID as the key, and another map as the value, 
                which contains the TF, IDF, and list of occurences(position). The text may or may not exist in the database,
                it is the responsibility of the data layer to update the existing entry.
    WorkFlow/Side Effect: Instead of directly replacing the entry with input given, 
                the function would first retrieve the existing data, loop through to check if in each entry of “documents”,
                the document ID associated with this word already exists, and if so, replace the entry with the input. 
                If not, add the non-existent entry to the map of “documents”.
    Output: true if added successfully, false if exceptions occur.
    Example Input:
        [
          {
             "text": "Lambda",
             "documents":
                 {
                     "5da65f292f67f000015296c": {
                         "tf": 0.308,
                         "idf": 2.996,
                         "occurrences": [1, 4, 10, 13]
                     }
        
                   "2kn3sdf0012nh19287560d": {
                       ....
                   }
               },
          }
         {
               "text": "Test",
               "documents": {....}
           } 
        ]
    '''

    def put(self, contents):
        # Currently just loop through the content and apply insert one
        # Later support insert many
        insert_ids = list()
        for content in contents:
            obj_id = self.collection.insert_one(content).inserted_id
            insert_ids.append(obj_id)
        return insert_ids

    '''
    Description: get a list of words from the database
    Parameters: texts is a list of words from the query.
    WorkFlow/Side Effect: Retrieve and directly return, no modification required in the database
    Output: A list of document mappings, with document ID as key, and a map of  TF, IDF, occurrence, etc as the value. 
            If the text could not be found in the database, an empty list is returned.
    Example output: Shows return value when input [“Lambda”, “Test”]
        [   
          "5da65f292f67f000015296c": {
                 "tf": 0.308,
                 "idf": 2.996,
                 "occurrences": [1, 4, 10, 13]
           },
    
          "2kn3sdf0012nh19287560d": {
                ....
           }    
        ]
    '''

    def get(self, texts):
        # Currently just search text one by one,
        # Later can apply find to search for multiple result
        result_list = list()
        for text in texts:
            query = {"text": text}
            count = self.collection.count_documents(query)
            print("there are {} document with {}".format(count, query))
            one = self.collection.find_one(query)
            result_list.append(one)
        return result_list

    '''
    Description: get_by_document get a word from the database with documentID specified
    Parameters: text is the word, documentID is the specific document ID
    WorkFlow/Side Effect: Retrieve and directly return, no modification in the database required.
    Output: A map containing the text, documentID, TF, IDF and occurrences(position) of the word in the document.
    Example output: Shows return value with “text” = “Lambda”, “documentID” = “5da65f292f67f000015296c”
        {
           "text": "Lambda",
           "documentID": "5da65f292f67f000015296c",
           "content": {
               "tf": 0.308,
               "idf": 2.996,
               "occurrences": [1, 4, 10, 13]
           }
        }
    '''

    def get_by_document(self, text, document):
        pass

    '''
    Description: Deletes occurrences of documentID for all words in the wordList. 
    Parameters: documentID is the identifying string for a specific document, wordList is a list of words that occur in that document.
    WorkFlow/Side Effect: 
                Loop through the wordList, and delete the entry in the documents list for the given word, 
                where the key is the specified documentID.
    Output: The documentID will be returned for a sanity check and “status” is the operation status. 
            If the delete operation is successful, the status code would be 1. 
            If the document is not found in any word in the wordList the code would be 0, 
            otherwise it would be -1 (detailed exception code type would be identified in later development).
    Example output:
        {
           "documentID": "5da65f292f67f000015296c",
           “status": <1, 0, -1>
        }
    '''

    def delete_document(self, document, word_list):
        pass

    def aggregation(self, text):
        group = self.collection.aggregate([
            {"$match": {"text": text}},
        ])

        return group

    def adv_aggregation(self):
        mapper = Code("""
            function () {
                emit(this.text, 1);
            }
        """)

        reducer = Code("""
            function (key, values) {
                var total = 0;
                for (var i = 0; i < values.length; i ++){
                    total += values[i];
                }
                return total;
            }
        """)

        result = self.collection.map_reduce(mapper, reducer, "my_results")
        print(result)
        for doc in result.find():
            pprint.pprint(doc)

    def adv_aggregation2(self):
        mapper = Code("""
            function () {
                emit(this.text, this.documents);
            }
        """)

        reducer = Code("""
            function (key, values) {
                var obj = {};
                for (var i = 0; i < values.length; i++) {
                    for(let key in values[i]){
                        obj[key] = values[i][key];
                    } 
                }
                return obj;
            }
        """)

        result = self.collection.map_reduce(mapper, reducer, "my_results2")
        print(result)
        for doc in result.find():
            pprint.pprint(doc)

    def remove_text(self, text):
        success = self.collection.delete_many({"text": text})
        print(success)


if __name__ == "__main__":
    # test local mongo db establishment
    word = [
        {
            "text": "Test2",
            "documents":
                {
                    "5da65f292f67f000015296c": {
                        "tf": 0.308,
                        "idf": 2.996,
                        "occurrences": [1, 4, 10, 13]
                    },

                    "2kn3sdf0012nh19287560d": {
                        "tf": 0.416,
                        "idf": 3.0,
                        "occurrences": [1, 4]
                    }
                }
        },
    ]

    dataLayer = DataLayer()
    dataLayer.put(word)
    results = dataLayer.get(["Lambda"])

    for result in results:
        pprint.pprint(result)

    print("------------------------try aggregate------------------------")
    results = dataLayer.aggregation("Lambda")
    for result in results:
        pprint.pprint(result)

    print("------------------------try map reduce------------------------")
    # results = \
    dataLayer.adv_aggregation()
    # for result in results.find():
    #     pprint.pprint(result)

    print("a new collection.........")
    client = MongoClient(HOST, PORT)
    collection = client[DATABASE]["my_results"]
    for result in collection.find():
        pprint.pprint(result)

    print("------------------------try adv map reduce------------------------")
    count = client[DATABASE]["my_results2"].count_documents({"_id": "Lambda"})
    print("there are {} doc with of text: Lambda in result2".format(count))
    dataLayer.adv_aggregation2()

    client = MongoClient(HOST, PORT)
    collection = client[DATABASE]["my_results2"]
    result = collection.find_one({"_id": "Test2"})
    pprint.pprint(result)
