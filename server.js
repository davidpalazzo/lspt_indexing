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
/*
Returns a list of documents that contains all documents that contain every word for a specific query.
requires at least one word
*/
app.post('/relevantDocsIntersection', function(req,res){
    // req.body is the document text transformation is sending to us
    let words = req.body.words;//array
    if (words.length<1){
        res.status(500).send("invalid body",req.body);
    }
    let intersectDocs = logicLayer.getDocumentsWithWord(words[0]);
    for( i = 1 ; i < words.length && intersectDocs.length>0 ; i++){
        //finds docs that have words[i] in it and 
        //intersects the resulting docs with the original set of docs
        let docsForWord = logicLayer.getDocumentsWithWord(words[i]);
        intersectDocs = intersectDocs.filter(value => docsForWord.includes(value));
    }
    res.status(200).send(documents);
});
/*
Returns a list of documents that contains all documents with any word of a specific query
*/
app.post('/relevantDocsUnion', function(req,res){
    // req.body is the document text transformation is sending to us
    let words = req.body.words;//array
    let documents;
    for( i = 0 ; i < words.length ; i++){
        documents.push(logicLayer.getDocumentsWithWord(words[i]));
    }
    res.status(200).send(documents);
 });
/*
Returns a list of documents that contain the query exactly
*/
app.post('/exactmatch', function(req,res){
    // req.body is the document text transformation is sending to us
    let words = req.body.words;//array
    let documents;
    if(words.length == 3){
        documents.push(logicLayer.getDocumentsWithTrigram(words));
    }else if(words.length == 2){
        documents.push(logicLayer.getDocumentsWithBigram(words));
    }else if(words.length == 1){
        documents.push(logicLayer.getDocumentsWithWord(words));
    }else{
        documents.push(logicLayer.getDocumentsWithNgram(words.length,words));    
    }res.status(200).send(documents);
    
});
// app.post('/docsInOrder', function(req,res){
//     // req.body is the document text transformation is sending to us

// });
// A call that either updates or adds indexing for a specific document.
//only existing document: 5da65f2592f67f000015296c
// app.post('/:id/all_words_and_ngrams', function(req,res){
//     // parse out words count and occurrence list, add to it and send it back
//     let id = req.params.id;
//     for( i = 0 ; i < req.body.Words.WordCounts.length ; i++){
//         // req.body is the document text transformation is sending to us
//         // FORM: https://lspt-fall-19.slack.com/files/UMWB42VHB/FNHBNHFFU/proglang-pa1.json?origin_team=TMTDVPRKP
//         let text = req.body.Words.WordCounts[i].Text;
//         let count = req.body.Words.WordCounts[i].Count;
//         let occurrences = req.body.Words.WordCounts.Occurences;
        
//         //we can find by text since text will be unique to each db entrance
//         collection.findOne({"text":text}, (dbWord)=>{
//             console.log(dbWord)//TODO: MongoError: no primary server available
//             let toSave = {"document":id,"count":count,"occurrences":occurrences}
//             dbWord.occurrences.push(toSave);
//             dbWord.save().catch((err)=>res.send({'err':err}))
//         }).catch((err)=>res.status(400).send(err));
//         //if document id is not in existing word, add toSave to word.occurrences
//         //else (id exists) idk what we should do
//     }
// });
// A call that either updates or adds indexing for a specific document.
//only existing document: 5da65f2592f67f000015296c
app.post('/:id/all_words_and_ngrams', function(req,res){
    // parse out words count and occurrence list, add to it and send it back
    let id = req.params.id;
    for( i = 0 ; i < req.body.Words.WordCounts.length ; i++){
        // req.body is the document text transformation is sending to us
        // FORM: https://lspt-fall-19.slack.com/files/UMWB42VHB/FNHBNHFFU/proglang-pa1.json?origin_team=TMTDVPRKP
        logicLayer.addDocument(req.body.Words.WordCounts[i])
        //SEND req.body.Words.WordCounts[i] TO logic layer
    }
});
/*
Things I need from logicLayer:
    logicLayer.addDocument(req.body.Words.WordCounts[i]);
    logicLayer.getDocumentsWithTrigram(words);
    logicLayer.getDocumentsWithBigram(words);
    logicLayer.getDocumentsWithWord(words);
    logicLayer.getDocumentsWithNgram(words.length,words);

*/

// launch our backend into a port
app.listen(PORT, () => console.log(`LISTENING ON PORT ${PORT}`));
