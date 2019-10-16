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


//using mongoose
// const uri = "mongodb://PEAKE:mongoDB1!@ds017175.mlab.com:17175/heroku_ht20w3xq";
// mongoose.connect( uri, { useNewUrlParser: true });
// const connection = mongoose.connection;
// connection.once('open', function() {
//     console.log("MongoDB database connection established successfully");
// })
// connection.on("error", console.error.bind(console, "MongoDB connection error:"));


app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// enable cors
// const cors = require('cors');
// app.use(cors());


app.post('/relevantDocsIntersection', function(req,res){
    // req.body is the document text transformation is sending to us

});
app.post('/relevantDocsUnion', function(req,res){
    // req.body is the document text transformation is sending to us

});
app.post('/exactmatch', function(req,res){
    // req.body is the document text transformation is sending to us

});
app.post('/docsInOrder', function(req,res){
    // req.body is the document text transformation is sending to us

});
//only existing document: 5da65f2592f67f000015296c
app.post('/:id/all_words_and_ngrams', function(req,res){
    // parse out words count and occurrence list, add to it and send it back
    let id = req.params.id;
    for( i = 0 ; i < length(req.body.Words.WordCounts) ; i++){
        // req.body is the document text transformation is sending to us
        // FORM: https://lspt-fall-19.slack.com/files/UMWB42VHB/FNHBNHFFU/proglang-pa1.json?origin_team=TMTDVPRKP
        let text = req.body.Words.WordCounts[i].Text;
        let count = req.body.Words.WordCounts[i].Count;
        let occurrences = req.body.Words.WordCounts.Occurences;
        
        //we can find by text since text will be unique to each db entrance
        collection.find({"text":text}).then((dbWord)=>{//TODO: where is db defined?
            let toSave = {id:{"count":count,"occurrences":occurrences}}
            dbWord.occurrences.push(toSave);
            dbWord.save().catch((err)=>res.send({'err':err}))
        }).catch((err)=>res.status(400).send(err));
        //if document id is not in existing word, add toSave to word.occurrences
        //else (id exists) idk what we should do
    }
});

// launch our backend into a port
app.listen(PORT, () => console.log(`LISTENING ON PORT ${PORT}`));

  client.close();
});