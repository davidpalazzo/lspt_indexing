# content of test_sample.py
import requests
import json
from unittest.mock import Mock, patch
from dataLayer import DataLayer

'''
A series of tests testing the add document function

'''

dl = DataLayer()

DATA1 = {
    "DocumentID": "test_1",
    "Words":{
        "NumWords": 8,
        "NumDistinctWords": 2,
        "WordCounts": [
            {
                "Text": "Lambda",
                "Count": 5,
                "Occurences":[
                    1,
                    2,
                    3,
                    4,
                    5
                ]
            },
            {
                "Text": "Cow",
                "Count": 3,
                "Occurences":[
                    10,
                    11,
                    12
                ]
            }
        ]
    },
    "NGrams":{
        "BiGrams":[

        ],
        "TriGrams":[

        ]
    }
}

DATA3 = {
    "DocumentID": "test_1",
    "Words":{
        "NumWords": 6,
        "NumDistinctWords": 2,
        "WordCounts": [
            {
                "Text": "Lambda",
                "Count": 4,
                "Occurences":[
                    1,
                    2,
                    3,
                    4
                ]
            },
            {
                "Text": "Cow",
                "Count": 2,
                "Occurences":[
                    10,
                    12
                ]
            }
        ]
    },
    "NGrams":{
        "BiGrams":[

        ],
        "TriGrams":[

        ]
    }
}


DATA2 = {
    "DocumentID": "test_2",
    "Words":{
        "NumWords": 9,
        "NumDistinctWords":3,
        "WordCounts":[
            {
                "Text": "Lambda",
                "Count":3,
                "Occurences":[
                    1,
                    3,
                    5
                ]
            },
            {
                "Text": "Cow",
                "Count": 3,
                "Occurences":[
                    8,
                    10,
                    12
                ]
            },
            {
                "Text": "Calculus",
                "Count": 3,
                "Occurences":[
                    2,
                    4,
                    6
                ]
            }
        ]
    },
    "NGrams":{
        "BiGrams":[
            {
                "Text": "Lambda Calculus",
                "Count":3,
                "Occurences":[
                    1,
                    3,
                    5
                ]
            }
        ],
        "TriGrams":[

        ]
    }
}

DATA4 = {
    "DocumentID":"test_2",
    "Words":{
        "NumWords": 7,
        "NumDistinctWords":3,
        "WordCounts":[
            {
                "Text": "Lambda",
                "Count":2,
                "Occurences":[
                    1,
                    3
                ]
            },
            {
                "Text": "Cow",
                "Count": 3,
                "Occurences":[
                    8,
                    10,
                    12
                ]
            },
            {
                "Text": "Calculus",
                "Count": 2,
                "Occurences":[
                    2,
                    4
                ]
            }
        ]
    },
    "NGrams":{
        "BiGrams":[
            {
                "Text": "Lambda Calculus",
                "Count":2,
                "Occurences":[
                    1,
                    4
                ]
            }
        ],
        "TriGrams":[

        ]
    }
}

DATA5 = {
    "DocumentID":"test_3",
    "Words":{
        "NumWords":6,
        "NumDistinctWords": 3,
        "WordCounts":[
            {
                "Text": "Cow",
                "Count":2,
                "Occurences":[
                    1,
                    4
                ]
            },
            {
                "Text": "Milk",
                "Count":2,
                "Occurences":[
                    2,
                    5
                ]
            },
            {
                "Text": "Good",
                "Count":2,
                "Occurences":[
                    3,
                    6
                ]
            }
        ]
    },
    "NGrams":{
        "BiGrams":[
            {
                "Text": "Cow Milk",
                "Count":2,
                "Occurences":[
                    1,
                    4
                ]
            },
            {
                "Text": "Milk Good",
                "Count":2,
                "Occurences":[
                    2,
                    5
                ]
            },
            {
                "Text": "Good Cow",
                "Count":1,
                "Occurences":[
                    3
                ]
            }
        ],
        "TriGrams":[
            {
                "Text":"Cow Milk Good",
                "Count":2,
                "Occurences":[
                    1,
                    4
                ]
            }
        ]
    }
}
DATA6= {
    "DocumentID":"test_3",
    "Words":{
        "NumWords":5,
        "NumDistinctWords": 3,
        "WordCounts":[
            {
                "Text": "Cow",
                "Count":2,
                "Occurences":[
                    1,
                    4
                ]
            },
            {
                "Text": "Milk",
                "Count":2,
                "Occurences":[
                    2,
                    5
                ]
            },
            {
                "Text": "Good",
                "Count":2,
                "Occurences":[
                    3
                ]
            }
        ]
    },
    "NGrams":{
        "BiGrams":[
            {
                "Text": "Cow Milk",
                "Count":2,
                "Occurences":[
                    1,
                    4
                ]
            },
            {
                "Text": "Milk Good",
                "Count":1,
                "Occurences":[
                    2
                ]
            },
            {
                "Text": "Good Cow",
                "Count":1,
                "Occurences":[
                    3
                ]
            }
        ],
        "TriGrams":[
            {
                "Text":"Cow Milk Good",
                "Count":1,
                "Occurences":[
                    1
                ]
            }
        ]
    }
}

def test_add_empty():
    '''
    test relevant on an empty database
    '''
    print("ADD TESTS")
    #API_ENDPOINT = 'http://localhost:5000/update'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    #test with cow
    #test with jump
    #test with fox
    #test with random
    to_add = {
        "add":DATA1
    }
    result = requests.post(API_ENDPOINT, json = to_add)
    print("Test empty")
    dl.debug_print_mr_collection()
    print(result.status_code)
    assert result.status_code == 200
    
def test_add_one_line():
    '''
    add parsed sample data to document see if all there
    do multiple adds
    try to add existing data
    '''
    #API_ENDPOINT = 'http://localhost:5000/update'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    #test with cow, returns documents 1 and 2
    #test with jumped, returns documents 1 and 3
    #test with fox, returns documents 3 and 4
    #test with random, returns no documents
    to_add = {
        "add":DATA1
    }
    to_add2 = {
        "add":DATA2
    }
    result = requests.post(API_ENDPOINT, json = to_add)
    result2 = requests.post(API_ENDPOINT, json = to_add2)
    print("Test one line")
    dl.debug_print_mr_collection()
    assert result.status_code == 200
    assert result2.status_code == 200
    
def test_add_multi_line():
    '''
    add parsed sample data to document see if all there
    do multiple adds
    try to add existing data
    '''
    #API_ENDPOINT = 'http://localhost:5000/update'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    to_add = {
        "add":DATA1
    }
    to_add_2 = {
        "add":DATA2
    }
    to_add_3 = {
        "add":DATA5
    }
    result = requests.post(API_ENDPOINT, json = to_add)
    result2 = requests.post(API_ENDPOINT, json = to_add_2)
    result3 = requests.post(API_ENDPOINT, json = to_add_3)
    print("Test multi line")
    dl.debug_print_mr_collection()
    assert result.status_code == 200
    assert result2.status_code == 200
    assert result3.status_code == 200

'''
A series of tests adding 
'''
def test_remove_empty():
    print("Remove Tests")
    '''
    test remove on an empty database
    '''
    #API_ENDPOINT = 'http://localhost:5000/update'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    to_remove = {
        "remove":DATA1
    }
    requests.post(API_ENDPOINT, json = to_remove)
    result = requests.post(API_ENDPOINT, json = to_remove)
    print("After empty")
    dl.debug_print_mr_collection()
    #all tests will return that database is empty
    assert result.status_code == 200

def test_remove_one_line():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
    #API_ENDPOINT = 'http://localhost:5000/update'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    #test with document1, all trace of document one removed
    #test with document1, document should not exist
    #test with document5, document should not exist
    #test with document3 and document4, remove all traces
    re_add = {
        "add":DATA1
    }
    remove = {
        "remove":DATA1
    }
    requests.post(API_ENDPOINT, json = re_add)
    result = requests.post(API_ENDPOINT, json = remove)
    print("After one line")
    dl.debug_print_mr_collection()
    assert result.status_code == 200

def test_remove_multiple_lines():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
    #API_ENDPOINT = 'http://localhost:5000/update'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    re_add = {
        "add":DATA1
    }
    remove = {
        "remove":DATA1
    }
    remove_2 = {
        "remove":DATA2
    }
    remove_3 = {
        "remove":DATA5
    }
    requests.post(API_ENDPOINT, json = re_add)
    result = requests.post(API_ENDPOINT, json = remove)
    result_2 = requests.post(API_ENDPOINT, json = remove_2)
    result_3 = requests.post(API_ENDPOINT, json = remove_3)
    print("After multi_line")
    dl.debug_print_mr_collection()
    assert result.status_code == 200
    assert result_2.status_code == 200
    assert result_3.status_code == 200
    
def test_update_empty():
    '''
    test update on empty database
    '''
    print("Update tests")
    #API_ENDPOINT = 'http://localhost:5000/update'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    #all tests will fail as it's empty
    to_update = {
        "remove":DATA1,
        "add":DATA3
    }
    print("update empty")
    result = requests.post(API_ENDPOINT, json = to_update)
    dl.debug_print_mr_collection()
    assert result.status_code == 200

def test_update_one_line():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
    #API_ENDPOINT = 'http://localhost:5000/update'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    #test with document1 without cow, cow should no longer be in d1
    #test with document2, without cow, cow should no lonber be in d2
    #test with document3, without white and fox, both should no longer be in d3
    #test with document4, without small, should no longer be in d4
    #attempt to update a document that doesn't exist, should return error
    to_remove = {
        "remove":DATA3
    }
    to_add = {
        "add":DATA1
    }
    to_update = {
        "remove":DATA1,
        "add":DATA3
    }
    print("update one line")
    requests.post(API_ENDPOINT, json = to_remove)
    requests.post(API_ENDPOINT, json = to_add)
    result = requests.post(API_ENDPOINT, json = to_update)
    dl.debug_print_mr_collection()
    assert result.status_code == 200

def test_update_multiplpe_line():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
    #API_ENDPOINT = 'http://localhost:5000/update'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    #test updating d1 multiple tiems
    #test updating d2 multiple times
    #test updating d3 multiple times
    to_add = {
        "add":DATA2
    }
    to_update = {
        "remove":DATA2,
        "add":DATA4
    }
    to_add_2 = {
        "add":DATA5
    }
    to_update_2 = {
        "remove":DATA5,
        "add":DATA6
    }
    print("update multi line")
    requests.post(API_ENDPOINT, json = to_add)
    result = requests.post(API_ENDPOINT, json = to_update)
    requests.post(API_ENDPOINT, json = to_add_2)
    result2 = requests.post(API_ENDPOINT, json = to_update_2)
    dl.debug_print_mr_collection()
    print(result.text)
    assert result.status_code == 200
    assert result2.status_code == 200

'''
A series of tests testing the relevant document function
It tests on an empty database, on single line documents, and multi-line documents
'''

REL_DATA = {
    "DocumentID":"data1",
    "Words":{
        "NumWords":5,
        "NumDistinctWords":2,
        "WordCounts":[
            {
                "Text": "Broccoli",
                "Count": 3,
                "Occurences":[
                    1,
                    2,
                    3
                ]
            },
            {
                "Text": "Good",
                "Count":2,
                "Occurences":[
                    4,
                    5
                ]
            }
        ]
    },
    "NGrams":{
        "BiGrams":[

        ],
        'TriGrams':[

        ]
    }
}

REL_DATA_2 = {
    "DocumentID":"data2",
    "Words":{
        "NumWords":8,
        "NumDistinctWords":2,
        "WordCounts":[
            {
                "Text": "Good",
                "Count": 4,
                "Occurences":[
                    1,
                    3,
                    5,
                    7
                ]
            },
            {
                "Text": "Food",
                "Count": 4,
                "Occurences":[
                    2,
                    4,
                    6,
                    8
                ]
            }
        ]
    },
    "NGrams":{
        "BiGrams":[
            {
                "Text": "Good Food",
                "Count": 4,
                "Occurences":[
                    1,
                    3,
                    5,
                    7
                ]
            },
            {
                "Text": "Food Good",
                "Count": 3,
                "Occurences":[
                    2,
                    4,
                    6
                ]
            }
        ],
        "TriGrams":[
            
        ]
    }
}

REL_DATA_3 = {
    "DocumentID":"data3",
    "Words":{
        "NumWords":6,
        "NumDistinctWords":3,
        "WordCounts":[
            {
                "Text": "Good",
                "Count":1,
                "Occurences":[
                    1
                ]
            },
            {
                "Text": "Coding",
                "Count":1,
                "Occurences":[
                    2
                ]
            },
            {
                "Text":"Practices",
                "Count":3,
                "Occurences":[
                    3
                ]
            }
        ]
    },
    "NGrams":{
            "BiGrams":[
                {
                    "Text": "Good Coding",
                    "Count":1,
                    "Occurences":[
                        1
                    ]
                },
                {
                    "Text": "Coding Practices",
                    "Count":1,
                    "Occurences":[
                        2
                    ]
                }
            ],
            "TriGrams":[
                {
                    "Text": "Good Coding Practices",
                    "Count":1,
                    "Occurences":[
                        1
                    ]
                }
            ]
    }
}

def clear_up(data_layer):
    data_layer.collection.delete_many({})
    data_layer.mr_collection.delete_many({})
    assert data_layer.collection.count_documents({}) == 0
    assert data_layer.mr_collection.count_documents({}) == 0
    data_layer.collection.drop()
    data_layer.mr_collection.drop()

def test_relevant_empty():
    '''
    test relevant on an empty database
    '''
    #API_ENDPOINT = 'http://localhost:5000/relevantDocs'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/relevantDocs'
    to_send = ["Cow"]
    response = requests.post(API_ENDPOINT, json=to_send)
    #response = requests.get(API_ENDPOINT)
    print(response.text)
    if response:
        print('Success!')
    else:
        print('error')
    print("gets here")
    #test with cow
    #test with jump
    #test with fox
    #test with random

def test_relevant_one_line():
    '''
    Returns single document
    Returns multiple documents
    Returns no documents as none exist
    '''
    #API_ENDPOINT = 'http://localhost:5000/relevantDocs'
    #API_ENDPOINT_ADD = 'http://localhost:5000/update'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/relevantDocs'
    API_ENDPOINT_ADD = 'http://lspt-index1.cs.rpi.edu:5000/update'
    test_data = {
        "add":REL_DATA
    }
    test_data_2 ={
        "add":REL_DATA_2
    }
    to_send_1 = ["Broccoli"]
    to_send_2 = ["Good"]
    requests.post(API_ENDPOINT_ADD, json = test_data)
    requests.post(API_ENDPOINT_ADD, json = test_data_2)
    dl.debug_print_mr_collection()
    response1 = requests.post(API_ENDPOINT, json=to_send_1) #return data 1
    print("After first post request")
    print(response1.text)
    response2 = requests.post(API_ENDPOINT, json=to_send_2) #return data 1 and 2
    print(response2.text)
    #dl.debug_print_mr_collection()
    #test with cow
    #test with jump
    #test with fox
    #test with random
    assert 1 == 1

def test_relevant_multi_line():
    '''
    Returns single document
    Returns multiple documents
    Returns no documents as none exist
    '''
    #API_ENDPOINT = 'http://localhost:5000/relevantDocs'
    #API_ENDPOINT_ADD = 'http://localhost:5000/update'
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/relevantDocs'
    API_ENDPOINT_ADD = 'http://lspt-index1.cs.rpi.edu:5000/update'
    test_data_3 = {
        "add": REL_DATA_3
    }
    to_send_1 = ["Good"]
    to_send_2 = ["Food"]
    to_send_3 = ["Practices"]
    to_send_4 = ["Good Food"]
    to_send_5 = ["Good Coding"]
    to_send_6 = ["Good Coding Practices"]
    requests.post(API_ENDPOINT_ADD, json=test_data_3)
    response1 = requests.post(API_ENDPOINT, json = to_send_1)#data1, data2, data3
    print(response1.text)
    response2 = requests.post(API_ENDPOINT, json = to_send_2)#data2
    print(response2.text)
    response3 = requests.post(API_ENDPOINT, json = to_send_3)#data3
    print(response3.text)
    response4 = requests.post(API_ENDPOINT, json = to_send_4)#data2
    print(response4.text)
    response5 = requests.post(API_ENDPOINT, json = to_send_5)#data3
    print(response5.text)
    response6 = requests.post(API_ENDPOINT, json = to_send_6)#data3
    print(response6.text)
6
def test_all():
    #test all commands here
    #return which ones fail, which ones don't
    #clear_up(dl)
    #test_add_empty()
    #test_add_one_line()
    #test_add_multi_line()
    #test_remove_empty()
    #test_remove_one_line()
    #test_remove_multiple_lines()
    #test_update_empty()
    #test_update_one_line()
    #test_update_multiplpe_line()
    #clear_up(dl)
    test_relevant_empty()
    print("After first test")
    test_relevant_one_line()
    print("After second test")
    #test_relevant_multi_line()
    print("After third test")

if __name__ == "__main__":
    test_all() 
