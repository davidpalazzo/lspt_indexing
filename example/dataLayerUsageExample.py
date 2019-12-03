import sys
sys.path.append("..")
import pprint
from dataLayer import DataLayer


def put_example(data_layer):
    data_layer.put(
        [
            {
                "text": "Lambda",
                "documentId": "1",
                "document":
                    {
                        "tf": 1,
                        "idf": 2,
                        "occurrences": [12, 17, 20]
                    }
            },

            {
                "text": "Lambda",
                "documentId": "2",
                "document":
                    {
                        "tf": 3,
                        "idf": 4,
                        "occurrences": [1, 4, 5]
                    }
            },
            {
                "text": "Test",
                "documentId": "2",
                "document":
                    {
                        "tf": 100,
                        "idf": 200,
                        "occurrences": [100]
                    }
            }
        ])


def get_example(data_layer):
    results = data_layer.get(["Lambda", "Test"])
    for result in results:
        pprint.pprint(result)


def delete_example(data_layer):
    print("delete documentId = {}, texts = [{}]:\n".format(2, "Lambda, Test"))
    data_layer.delete_text("2", ["Lambda", "Test"])


def clear_up(data_layer):
    data_layer.collection.delete_many({})
    data_layer.mr_collection.delete_many({})
    assert data_layer.collection.count_documents({}) == 0
    assert data_layer.mr_collection.count_documents({}) == 0
    data_layer.collection.drop()
    data_layer.mr_collection.drop()


if __name__ == "__main__":
    dataLayer = DataLayer()

    put_example(dataLayer)
    print("=================Applied put example============================")
    get_example(dataLayer)
    print("=================Applied delete example============================")
    delete_example(dataLayer)
    get_example(dataLayer)

    # this function just to clear up the things just added
    clear_up(dataLayer)
