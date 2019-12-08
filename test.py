# content of test_sample.py
import requests
import json
from unittest.mock import Mock, patch

'''
A series of tests testing the add document function

'''

DATA1 = {
    "Words":{
        "NumWords": 20,
        "NumDistinctWords": 10,
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
                "Count": 5,
                "Occurences":[
                    10,
                    11,
                    12
                ]
            }
        ]
    }
}

DATA3 = {
    "Words":{
        "NumWords": 20,
        "NumDistinctWords": 10,
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
    }
}


DATA2 = {
    "Words":{
        "NumWords": 40,
        "NumDistinctWords":30,
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
        "Bigrams":[
            {
                "Text": "Lambda Calculus",
                "Count":3,
                "Occurences":[
                    1,
                    3,
                    5
                ]
            }
        ]
    }
}

DATA4 = {
    "Words":{
        "NumWords": 40,
        "NumDistinctWords":30,
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
        "Bigrams":[
            {
                "Text": "Lambda Calculus",
                "Count":2,
                "Occurences":[
                    1,
                    4
                ]
            }
        ]
    }
}

DATA5 = {
    "Words":{
        "NumWords":40,
        "NumDistinctWords": 25,
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
        "Bigrams":[
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
        "Trigrams":[
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
    "Words":{
        "NumWords":40,
        "NumDistinctWords": 25,
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
        "Bigrams":[
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
        "Trigrams":[
            {
                "Text":"Cow Milk Good",
                "Count":1,
                "Occurences":[
                    1,
                ]
            }
        ]
    }
}

def test_add_empty():
    '''
    test relevant on an empty database
    '''
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    #test with cow
    #test with jump
    #test with fox
    #test with random
    to_add = {
        "add":DATA1
    }
    result = requests.post(API_ENDPOINT, json = to_add)
    print(result.status_code)
    assert result.status_code == 200
    
def test_add_one_line():
    '''
    add parsed sample data to document see if all there
    do multiple adds
    try to add existing data
    '''
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    #test with cow, returns documents 1 and 2
    #test with jumped, returns documents 1 and 3
    #test with fox, returns documents 3 and 4
    #test with random, returns no documents
    to_add = {
        "add":{DATA1}
    }
    to_add2 = {
        "add":{DATA2}
    }
    result = requests.post(API_ENDPOINT, json = to_add)
    result2 = requests.post(API_ENDPOINT, json = to_add2)
    assert result.status_code == 200
    assert result2.status_code == 200
    
def test_add_multi_line():
    '''
    add parsed sample data to document see if all there
    do multiple adds
    try to add existing data
    '''
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    to_add = {
        "add":{DATA1}
    }
    to_add_2 = {
        "add":DATA2
    }
    to_add_3 = {
        "add":{DATA3}
    }
    result = requests.post(API_ENDPOINT, json = to_add)
    result2 = requests.post(API_ENDPOINT, json = to_add_2)
    result3 = requests.post(API_ENDPOINT, json = to_add_3)
    assert result == "update post recieved"

'''
A series of tests adding 
'''
def test_remove_empty():
    '''
    test remove on an empty database
    '''
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    to_add = {
        "remove":DATA1
    }
    result = requests.post(API_ENDPOINT, json = to_add)
    result_dup = requests.post(API_ENDPOINT, json = to_add)
    #all tests will return that database is empty
    assert 1 == 1

def test_remove_one_line():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
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
    print("data removed")
    result = requests.post(API_ENDPOINT, json = remove)
    assert result == "update post recieved"

def test_remove_multiple_lines():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
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
        "remove":DATA3
    }
    requests.post(API_ENDPOINT, json = re_add)
    result = requests.post(API_ENDPOINT, remove)
    result_2 = requests.post(API_ENDPOINT, remove_2)
    result_3 = requests.post(API_ENDPOINT, remove_3)
    assert result == "update post recieved"
    
def test_update_empty():
    '''
    test update on empty database
    '''
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    #all tests will fail as it's empty
    to_update = {
        "remove":DATA1,
        "add":DATA3
    }
    print("gets here")
    result = requests.post(API_ENDPOINT, json = to_update)
    assert result == "update post recieved"

def test_update_one_line():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    #test with document1 without cow, cow should no longer be in d1
    #test with document2, without cow, cow should no lonber be in d2
    #test with document3, without white and fox, both should no longer be in d3
    #test with document4, without small, should no longer be in d4
    #attempt to update a document that doesn't exist, should return error
    to_add = {
        "add":{DATA1}
    }
    to_update = {
        "remove":{DATA1},
        "add":{DATA3}
    }
    result = requests.post(API_ENDPOINT, json = to_add)
    result = requests.post(API_ENDPOINT, json = to_update)
    assert result == "update post recieved"

def test_update_multiplpe_line():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/update'
    #test updating d1 multiple tiems
    #test updating d2 multiple times
    #test updating d3 multiple times
    to_add = {
        "add":{DATA2}
    }
    to_update = {
        "remove":{DATA2},
        "add":{DATA4}
    }
    to_add_2 = {
        "add":{DATA5}
    }
    to_update_2 = {
        "remove":{DATA5},
        "add":{DATA6}
    }
    result = requests.post(API_ENDPOINT, json = to_add)
    result = requests.post(API_ENDPOINT, json = to_update)
    result = requests.post(API_ENDPOINT, json = to_add_2)
    result = requests.post(API_ENDPOINT, json = to_update_2)
    assert result == "update post recieved"

'''
A series of tests testing the relevant document function
It tests on an empty database, on single line documents, and multi-line documents
'''

REL_DATA = {
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
    }
}

REL_DATA_2 = {
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
        "Bigram":[
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
        ]
    }
}

REL_DATA_3 = {
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
            "Bigrams":[
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
            "Trigrams":[
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

def test_relevant_empty():
    '''
    test relevant on an empty database
    '''
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/relevantDocs'
    #API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000'

    to_send = ["lspt"]
    to_send = ["homework"]
    response = requests.post(API_ENDPOINT, json=to_send)
    #response = requests.get(API_ENDPOINT)
    print(response)
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
    API_ENDPOINT = 'http://lspt-index1.cs.rpi.edu:5000/relevantDocs'
    API_ENDPOINT_ADD = 'http://lspt-index1.cs.rpi.edu:5000/update'
    test_data = {
        "add": REL_DATA
    }
    test_data_2 ={
        "add": REL_DATA_2
    }
    to_send_1 = ["Broccoli"]
    to_send_2 = ["Good"]
    requests.post(API_ENDPOINT_ADD, json = test_data)
    requests.post(API_ENDPOINT_ADD, json = test_data_2)
    response1 = requests.post(API_ENDPOINT, json=to_send_1) #return data 1
    responde2 = requests.post(API_ENDPOINT, json=to_send_2) #return data 1 and 2
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
    response = requests.post(API_ENDPOINT_ADD, json=test_data_3)
    respone1 = requests.post(API_ENDPOINT, json = to_send_1)
    respone2 = requests.post(API_ENDPOINT, json = to_send_2)
    respone3 = requests.post(API_ENDPOINT, json = to_send_3)
    respone4 = requests.post(API_ENDPOINT, json = to_send_4)
    respone5 = requests.post(API_ENDPOINT, json = to_send_5)
    respone6 = requests.post(API_ENDPOINT, json = to_send_6)
    assert 1 == 1

def test_all():
    #test all commands here
    #return which ones fail, which ones don't
    test_add_empty()
    test_add_one_line()
    test_add_multi_line()
    test_remove_empty
    test_remove_one_line()
    test_remove_multiple_lines()
    test_update_empty()
    test_update_one_line()
    test_update_multiplpe_line()
    test_relevant_empty()
    test_relevant_one_line()
    test_relevant_multi_line()

if __name__ == "__main__":
    test_all() 