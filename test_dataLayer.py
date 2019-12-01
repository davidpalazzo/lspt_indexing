import pytest
from pymongo import MongoClient
from dataLayer import DataLayer, DataBaseCreateFail

PORT = 27017
HOST = "localhost"
TEST_DB = "test_storage"
TEST_COLLECTION = "test-collection-4"
TEST_COLLECTION_MR = "test-map-reduce-4"
DATA = {
    "content1": {
        "text": "Lambda",
        "documentId": "1",
        "document":
            {
                "tf": 1,
                "idf": 2,
                "occurrences": [12, 17, 20]
            }
    },

    "content2": {
        "text": "Lambda",
        "documentId": "2",
        "document":
            {
                "tf": 3,
                "idf": 4,
                "occurrences": [1, 4, 5]
            }
    },

    "content3": {
        "text": "Lambda",
        "documentId": "2",
        "document":
            {
                "tf": 3,
                "idf": 4,
                "occurrences": [1, 4]
            }
    },

    "content4": {
        "text": "Test",
        "documentId": "2",
        "document":
            {
                "tf": 100,
                "idf": 200,
                "occurrences": [100]
            }
    }
}


class Queries:
    def __init__(self, contents):
        queries = set()
        self.expected_list = list()
        for content in contents:
            queries.add(content["text"])
            self.expected_list.append(content)
        self.queries = list(queries)

    def get_queries_list(self):
        return self.queries

    def get_expected_list(self):
        return self.expected_list


class Critical_data:
    def __init__(self, text, doc_id, tf, idf, occurrence):
        self.text = text
        self.doc_id = doc_id
        self.tf = tf
        self.idf = idf
        self.occurrence = occurrence

    def is_equal(self, critical_data):
        return self.text == critical_data.text and \
               self.doc_id == critical_data.doc_id and \
               self.tf == critical_data.tf and \
               self.idf == critical_data.idf and \
               self.occurrence == critical_data.occurrence

    def to_string(self):
        return "text: " + self.text + \
               "\ndoc_id: " + self.doc_id + \
               "\ntf: " + str(self.tf) + \
               "\nidf: " + str(self.idf) + \
               "\noccurrences" + str(self.occurrence)


def extract_data_from_collection(contents):
    results = list()
    for content in contents:
        data = Critical_data(content["text"],
                             content["documentId"],
                             content["document"]["tf"],
                             content["document"]["idf"],
                             content["document"]["occurrences"])
        results.append(data)
    return results


def extract_data_from_mr_collection(contents):
    results = list()
    for content in contents:
        text = content["_id"]
        documents = content["value"]["documents"]
        for document in documents:
            results.append(
                Critical_data(text,
                              document,
                              documents[document]["tf"],
                              documents[document]["idf"],
                              documents[document]["occurrences"]))
    return results


def get_db_instance():
    return DataLayer(TEST_DB, TEST_COLLECTION, TEST_COLLECTION_MR)


def get_db_accessor():
    # accessing the collection through host and port
    client = MongoClient(HOST, PORT)
    # retrieve the collection from data base
    collection = client[TEST_DB][TEST_COLLECTION]
    mr_collection = client[TEST_DB][TEST_COLLECTION_MR]
    return collection, mr_collection


def is_in(result, expected_list):
    for expected in expected_list:
        if result.is_equal(expected):
            return True
    return False


def helper_test_put(contents, expected_collection_count, expected_mr_collection_count):
    clear_up()

    try:
        data_layer = get_db_instance()
        data_layer.put(contents)
        expected_list = extract_data_from_collection(contents)
        collection, mr_collection = get_db_accessor()

        collection_count = collection.count_documents({})
        assert collection_count == expected_collection_count

        results = extract_data_from_collection(collection.find({}))
        for result in results:
            assert is_in(result, expected_list)

        mr_collection_count = mr_collection.count_documents({})
        assert mr_collection_count == expected_mr_collection_count

        results = extract_data_from_mr_collection(mr_collection.find({}))
        for result in results:
            assert is_in(result, expected_list)

        # results = mr_collection.find({})
        # for result in results:
        #     pprint.pprint(result)

    except DataBaseCreateFail:
        pytest.fail("Fail to create data base")


def test_put():
    same_text_diff_id = [DATA["content1"], DATA["content2"]]
    helper_test_put(same_text_diff_id, 2, 1)

    multiple_text = [DATA["content1"], DATA["content2"], DATA["content4"]]
    helper_test_put(multiple_text, 3, 2)

    update_document = [DATA["content1"], DATA["content2"], DATA["content3"]]
    helper_test_put(update_document, 2, 1)


def helper_test_get(contents, queries):
    clear_up()

    try:
        data_layer = get_db_instance()
        data_layer.put(contents)
        # get the list from map reduce collection, and extract the message critical message

        results = data_layer.get(queries.get_queries_list())
        results = extract_data_from_mr_collection(results)

        for result in results:
            assert is_in(result, extract_data_from_collection(queries.get_expected_list()))

    except DataBaseCreateFail:
        pytest.fail("Fail to create data base")


def test_get():
    contents = [DATA["content1"], DATA["content2"], DATA["content3"], DATA["content4"]]
    queries = Queries(contents)
    helper_test_get(contents, queries)


def helper_test_delete(data_layer, document_id, text):
    collection, mr_collection = get_db_accessor()

    pre_results = extract_data_from_mr_collection(mr_collection.find({"_id": text}))

    data_layer.delete_text(document_id, [text])
    assert collection.count_documents({"text": text, "documentId": document_id}) == 0

    after_results = extract_data_from_mr_collection(mr_collection.find({"_id": text}))

    for result in pre_results:
        if result.text == text and result.doc_id == document_id:
            assert not is_in(result, after_results)
            continue
        assert is_in(result, after_results)


def test_delete():
    clear_up()

    contents = [DATA["content1"], DATA["content2"], DATA["content3"], DATA["content4"]]

    try:
        data_layer = get_db_instance()
        data_layer.put(contents)

        helper_test_delete(data_layer, "2", "Lambda")
        helper_test_delete(data_layer, "2", "Test")
        helper_test_delete(data_layer, "1", "Lambda")

    except DataBaseCreateFail:
        pytest.fail("Fail to create data base")


def clear_up():
    # get the collections from accessor
    collection, mr_collection = get_db_accessor()
    # remove the content and drop the tables
    collection.delete_many({})
    mr_collection.delete_many({})
    assert collection.count_documents({}) == 0
    assert mr_collection.count_documents({}) == 0
    collection.drop()
    mr_collection.drop()
