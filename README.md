How to use server.js (api)
1. you need node
2. make sure you have no other node processess running on port 5000
	- to kill all node processes:  pkill nodejs or pkill node
3. run node server.js


###Testing apis:
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