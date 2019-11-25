// const keys = require("config.js"); for secret keys if needed later
const mongoose = require("mongoose");
const express = require("express");
const bodyParser = require("body-parser");

const PORT = process.env.PORT || 5000;
const app = express();
let Word = require('./model.word');   // import models used to store information
//do we need a Document model?
 
//using mongo client
const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://LSPIndexing:LSPIndexing@largescaleindexing-lsdil.mongodb.net/test?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true });
var collection;
client.connect(err => {
  collection = client.db("LargeScaleIndex").collection("index");
 // perform actions on the collection object


app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// enable cors
// const cors = require('cors');
// app.use(cors());

/*
test route to check for connection
*/
app.get('/',function(req,res){
    res.status(200).send({'hello':"world"});
})
/*POST (/’relevantDocs) FROM RANKING
BODY:
[“NGRAM1”,”NGRAM2”,...]
RESPONSE:
{
   “NGRAM1”:
    [
       “Documentid1”:{documentData},
       “Documentid1”: {documentData},...
    ],
    “NGRAM2”:...
}
Where documentData is of form: 
{
   "tf": INT,
   "idf" : INT,
   "tf-idf" : INT
 }
 */
app.post('/relevantDocs', function(req,res){
	console.log("body received:", req.body)
	res.status(200).send("relevant docs post recieved")
})
/*POST: ‘/update’ FROM DDS
BODY: 
If only remove provided, we assume it is a remove
If only add provided, we assume it is an add
If both are provided, we assume it is an update
{
   "add": {documentData},
   "remove" : {documentData}
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
*/
app.post("/update", function(req,res){
	console.log("body recieved",req.body)
	res.status(200).send("update post recieved")
})


// launch our backend into a port
app.listen(PORT, () => console.log(`LISTENING ON PORT ${PORT}`));
});