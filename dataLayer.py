import pymongo
from bson.code import Code
from pymongo import MongoClient
import time
import pprint

PORT = 27017
HOST = "localhost"
DATABASE = "indexing"
COLLECTION = "texts"
COLLECTION_MR = "texts_collection"

"""
DataLayer provides a wrapper for accessing the collection, 
and is designed for handling concurrent operation:
Having two collection to store contents in order to allow atomic operation
Apply incremental map-reduce mechanism for updating collection 1 to collection 2
Incremental apply time stamp for storing the update

Collection 1 has unique compound key on "text" and "documentId", which means if the "text" is the same
but with different "documentId", it still allow to store both information. When doing add, entry will be directly
added in to the collection using the format shown as following if the compound key does not exist, otherwise,
update will applied, and also renew the timestamp. 
This allow atomic operation on individual entry when doing add, update, remove and etc.

Collection 1 Example:
content1 and content2 can exist in collection 1 at the same time, after done with the 'put' operation,
map reduce would be applied to aggregate the newly inserted/updated entry into the collection 2.

content1 = {
            "text": "my_word",
            "ts": "20190817xxxx"
            "documentId": 5da65f292f67f000015296c,
            "document": {
                "tf": 0.308,
                "occurrences": [1, 4, 10, 13]
            } 
        }

content2 = {
            "text": "my_word",
            "ts": "20190817xxxx"
            "documentId": 2kn3sdf0012nh19287560d,
            "document": {
                "tf": 0.416,
                "occurrences": [1, 4]
            } 
        }

Collection 2 is handled by map reduce, incrementally map the newly added or updated entry from collection 1,
and do reduce to the mapped entry from collection 1 and the already existed entry from collection 2.
Map reduce provided by mongodb should be considered as thread safe.

Collection 2 Example:
The following example shown outcome of applying map reduce on content1 and content2

{
    "_id": "my_word",
    "value": {
        "documents": {
            "5da65f292f67f000015296c":
            {
                "tf": 0.308,
                "occurrences": [1, 4, 10, 13]
                "ts": "20190817xxxx",   # the last time update 
            },

            "2kn3sdf0012nh19287560d":
            { 
                "tf": 0.416,
                "occurrences": [1, 4]
                "ts": "20190817xxxx",   # the last time update 
            }
        }
    }
}
"""


class DataLayer:
    """
    constructor for DataLayer, provide a way for user declare the database to used and
    the name of the two collections. Check the default deceleration above
    """

    def __init__(self, db=DATABASE, collection=COLLECTION, mr_collection=COLLECTION_MR):

        try:
            # get the client from default host and port
            client = MongoClient(HOST, PORT)
            # create/accessing the database collection
            self.collection = client[db][collection]
            # create/accessing the database collection for map reduce
            self.mr_collection = client[db][mr_collection]

            # create the unique compound index on text and documentId in decreasing order
            success = self.collection.create_index([("text", pymongo.ASCENDING),
                                                    ("documentId", pymongo.ASCENDING)], unique=True)
            if not success:
                raise DataBaseCreateFail()

        except Exception:
            # catching the potential exception and
            # throw new exception indicating the failure on initialize stage
            raise DataBaseCreateFail()

    def put(self, contents):
        """
        put method puts a list of contents to the collection1,
        then applied map reduce on the newly updated entry, then stores the result to collection2.
        exception will through
        example_contents =
        [
            {
                "text": "Test2",
                "documentId": "5da65f292f67f000015296c",
                "document":
                {
                    "tf": 0.301,
                    "occurrences": [1, 100]
                }
            },

            {
                 "text": "Lambda",
                 "documentId": "2kn3sdf0012nh19287560d",
                 "document":
                 {
                    "tf": 0.416,
                    "occurrences": [1, 4]
                 }
            }
        ]
        :param contents: a list of contents. Every content has "text", "documentId", "document" as field,
        where "document" map to an object with "tf", "occurrences" as field.
        :return: True if all insert success, if one fail, raise DataBasePutFail Exception
        """
        try:
            # get the current time, map reduce will do mapping on the entry
            # with time latter then the current time
            last_update = time.time()
            for content in contents:
                # check if the content matches the require format
                if "text" not in content or \
                        "documentId" not in content or \
                        "document" not in content or \
                        "tf" not in content["document"] or \
                        "occurrences" not in content["document"]:
                    raise DataBasePutFail()

                # update the content to collection
                self.collection.update_one(
                    {"text": content["text"], "documentId": content["documentId"]},
                    {"$set": {"ts": time.time(), "document": content["document"]}},
                    upsert=True
                )
            self.map_reduce_aggregation(last_update)
            return True
        except Exception:
            raise DataBasePutFail()

    def map_reduce_aggregation(self, last_update):
        """
        map_reduce_aggregation will be called by the put when every update happen.
        map the newly update entry in collection1 and reduce with existing entry in collection2
        the example outcome in collection2 shown at the top
        :param last_update: specified timestamp to define the newly updated content. map reduce will
        only be applied on the content with timestamp larger last_update.
        :return: the result of map reduce, if fail, throw DataBaseAggregationFail which extends DataBasePutFail Exception
        """
        try:
            # define the mapper,
            # emit the key and value to be used in reducer
            # the mapper should have the same form with reduced value
            mapper = Code(
                '''
                function () {
                    // key is the text, value map "documents" to the object with 
                    // documentId as key and "document" in collection1 as content
                    // also, move add timestamp into the "document" field
                    var key = this.text;
                    var value = {"documents": {}}
                    value["documents"][this.documentId] = this.document;
                    value["documents"][this.documentId]["ts"] = this.ts;
                    
                    // emit the mapped key and value
                    emit(key, value);
                }
                '''
            )

            # define the reducer,
            # the reducer should always remain the same format no matter
            # how many times map reduce applied
            reducer = Code(
                '''
                // receive the key and value from the mapper
                function (key, values) {
                    // define new object to receive and add the newly reduced content
                    var obj = {};
                    obj["documents"] = {};
                    
                    // merge function check the timestamp of given documentId and document
                    // replace the existing content if the timestamp is larger
                    function merge(documentId, document) {
                        // check if the documentId is in the object
                        // if does, replace with new content
                        if (documentId in obj["documents"] &&
                            obj["documents"][documentId]["ts"] > document["ts"]) {
                            return;
                        }
                        obj["documents"][documentId] = document;
                    }
                    
                    // loop through the value collected, and apply merge on each documentId
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

            # apply map reduce using the mapper and reducer, with specified newly the time stamp
            return self.collection.map_reduce(mapper, reducer,
                                              out={"reduce": self.mr_collection.name},
                                              query={"ts": {"$gte": last_update}},
                                              )
        except Exception:
            raise DataBaseAggregationFail()

    def delete_text(self, document_id, texts):
        """
        delete_text delete the given document_id with a list of text.
        :param document_id: the id of the document
        :param texts: a list of text need to delete the entry of specified documentId
        :return: none. if exception happen, throw DataBaseDeleteFail
        """
        try:
            # loop through the text, and unset the document_id
            for text in texts:
                # delete the mr collection first
                self.mr_collection.update_one(
                    {"_id": text},
                    {"$unset": {"value.documents." + document_id: ""}}
                )
                # then delete the collection
                self.collection.delete_one({"text": text, "documentId": document_id})
        except Exception:
            raise DataBaseDeleteFail()

    def get(self, texts):
        """
        get method gets the a list of text from database,
        If one of the text does not exist, None value will be included
        return value is a list of result retrieve from
        collection2 directly with the following format:
        [
            {
                "_id": "my_word",
                "value": {
                    "documents": {
                        "5da65f292f67f000015296c":
                        {
                            "tf": 0.308,
                            "idf": 2.996,
                            "occurrences": [1, 4, 10, 13]
                            "ts": "20190817xxxx",
                        },

                        "2kn3sdf0012nh19287560d":
                        {
                            "tf": 0.416,
                            "idf": 3.0,
                            "occurrences": [1, 4]
                            "ts": "20190817xxxx",
                        }
                    }
                }
            },
            {....},
            None
        ]
        :param texts: is a list of text, for example ["my_word", "lambda", "test"].
        :return: a list of result, if text does not exist, None value will be included
        """
        try:
            # define a result list
            result_list = list()
            # loop through text list and do query on each text
            for text in texts:
                query = {"_id": text}
                # assert the content is unique with "_id"
                assert (self.mr_collection.count_documents(query) <= 1)
                one = self.mr_collection.find_one(query)
                if one is None:
                    one = {"_id": text, "value": {"documents": {}}}
                result_list.append(one)
            return result_list
        except Exception:
            raise DataBaseCreateFail()

    def debug_print_collection(self):
        """
        print all the collection for debug only
        """
        print("document found in collection: {}".format(self.collection.count_documents({})))
        for result in self.collection.find({}):
            pprint.pprint(result)

    def debug_print_mr_collection(self):
        """
        print all the mr collection for debug only
        """
        print("document found in collection: {}".format(self.collection.count_documents({})))
        for result in self.mr_collection.find({}):
            pprint.pprint(result)


"""
Exception Handling Hierarchy:
    Exception
        |__ DataBaseException
                    |__ DataBaseCreateFail
                    |__ DataBaseGetFail
                    |__ DataBaseDeleteFail
                    |__ DataBasePutFail
                            |__ DataBaseAggregationFail
"""


class DataBaseException(Exception):
    """
    DataBaseException is the parent
    exception for all data layer exception.
    User is able to use except DataBaseException to catch all
    types of database exception
    """

    def __init__(self):
        self.message = "Fail operate on database"


class DataBaseCreateFail(DataBaseException):
    """
    DataBaseCreateFail extends DataBaseException
    would be throw when creation of database fail.
    This caused by not running of mongodb or other specified by mongodb
    """

    def __init__(self):
        self.message = "Fail to create or access database"


class DataBaseGetFail(DataBaseException):
    """
    DataBaseGetFail extends DataBaseException
    would be throw when get request fail
    """

    def __init__(self):
        self.message = "Fail to do get request to database"


class DataBaseDeleteFail(DataBaseException):
    """
    DataBaseDeleteFail extends DataBaseException
    would be throw when delete request fail
    """

    def __init__(self):
        self.message = "Fail to do delete request to database"


class DataBasePutFail(DataBaseException):
    """
    DataBasePutFail extends DataBaseException
    would be throw when put request fail
    """

    def __init__(self):
        self.message = "Fail to do put request to database"


class DataBaseAggregationFail(DataBasePutFail):
    """
    DataBaseAggregationFail is extend DataBasePutFail
    would be throw when map reduce fail
    """

    def __init__(self):
        self.message = "Fail to aggregate data in database"
