AS OF 11/18, 11:01AM
POST (/’relevantDocs)
bSummary: Use this route to get a list of documents and scores for each n-gram provided.
Workflow: Ranking will receive a query request from the user and request relevant documents from us after breaking the query into multiple n-grams.
From: Ranking
ERR handling: if the list of n-grams is null or non-existing, we will assume it is an error and do no work.
BODY:
[“NGRAM1”,”NGRAM2”,...]
RESPONSE:
{
   “NGRAM1”:
    {
       “Documentid1”:{documentData},
       “Documentid1”: {documentData},...
    },
    “NGRAM2”:...
}
Where documentData is of form: 
{
   "tf": INT,
   "idf" : INT,
   "tf-idf" : INT
 }


POST: ‘/update’ 
Summary: Use this route to add, update, or remove a document when information pertaining to said document has changed.
Workflow: Crawling will determine if a document is to be added, updated, or removed, and Document Data Store will give us the data for the document that has been added, that needs to be removed, or both in the case of an update.
From: Document Data Store
ERR handling: if documentData is null rather than non-existing, we will assume it is an error and do no work.
BODY: 
If only remove provided, we assume it is a remove
If only add provided, we assume it is an add
If both are provided, we assume it is an update
For an update:
{
   "add": {documentData},
   "remove" : {documentData}
 }
For a remove:
{
   "remove" : {documentData}
 }
For an add:
{
   "add" : {documentData}
 }

Where document data is of form:
{
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
            },
            {
                "Text": "Calculus",
                "Count": 3,
                "Occurences": [
                    5,
                    19,
                    134
                ]
            },
            {
                "Text": "Haskell",
                "Count": 6,
                "Occurences": [
                    190,
                    204,
                    450,
                    560,
                    590,
                    610,
                    614
                ]
            }
        ]
    },
    "NGrams": {
        "BiGrams": [
            {
                "Text": "Lambda Calculus",
                "Count": 3,
                "Occurences": [
                    1,
                    4,
                    10,
                    13,
                    400,
                    590
                ]
            },
            {
                "Text": "Programming Assigment",
                "Count": 1,
                "Occurences": [
                    12
                ]
            }
        ],
        "TriGrams": [
            {
                "Text": "Lambda Calculus Interpreter",
                "Count": 2,
                "Occurences": [
                    40,
                    59
                ]
            }
        ]
    }
}
RESPONSE:
none


