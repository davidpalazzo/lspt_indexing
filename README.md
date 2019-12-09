### How to test:
you must have installed pytest through pip:
```pip install pytest```
write test cases in test.py


### How to use server.js (api) locally
1. you need node
2. make sure you have no other node processess running on port 5000
	- to kill all node processes:  `pkill nodejs` or `pkill node`
3. run `node server.js`

### How to use app.py(instead of server.js)
1. you need pip3, flask, python3
2. run`export FLASK_APP=app.py`
3. run `flask run`

### How to ssh for mac/linux
1. write `ssh your_username@lspt-index1.cs.rpi.edu`
2. you will be prompted to put in a password. it was given in an email with subject: csci4460

### How to connect for windows
1. get Chrome extension called secure shell app by google
2. launch it
3. use rcsid for username
4. hostname is lspt-index1.cs.rpi.edu
5. password is also in email with subject: csci4460

### PEP8 links
https://dev.to/j0nimost/setting-up-pep8-and-pylint-on-vs-code-34h
https://pypi.org/project/pep8/

### Testing apis:
for ```app.post('/:id/all_words_and_ngrams'```
use following as body on restlet/postman at localhost:5000
```{
    "URL": "https://www.cs.rpi.edu/academics/courses/fall19/proglang/pa1/pa1.html",
    "AsOfDate": "2019-09-26T12:55:21.000Z",
    "Meta": {
        "Title": "Programming Assignment #1",
        "Author": "Carlos Varela",
        "DateCreated": "2019-09-13T14:20:21.000Z",
        "DateModified": "2019-09-13T14:20:21.000Z",
        "KeyWords": [
            "Lambda",
            "Calculus",
            "Assignment",
            "Haskell",
            "Oz",
            "Carlos Varela"
        ]
    },
    "Words": {
        "NumWords": 12300,
        "NumDistinctWords": 5031,
        "WordCounts": [
            {
                "Text": "Lambda",
                "Count": 5,
                "Occurences": [
                    1,
                    4,
                    10,
                    13,
                    400,
                    590
                ]
            }
            
        ]
    }
}```
