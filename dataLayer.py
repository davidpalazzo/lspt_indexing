# let Word = require('./model.word');   // import models used to store information
# //do we need a Document model?
 
# //using mongo client
# const MongoClient = require('mongodb').MongoClient;
# const uri = "mongodb+srv://LSPIndexing:LSPIndexing@largescaleindexing-lsdil.mongodb.net/test?retryWrites=true&w=majority";
# const client = new MongoClient(uri, { useNewUrlParser: true });
# var collection;
# client.connect(err => {
#   collection = client.db("LargeScaleIndex").collection("index");

#   client.close();
# });
#####################################################################################
# above is the js code that needs to be translated to py 
#####################################################################################