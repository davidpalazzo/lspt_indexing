import json
import sqlite3
from flask import Flask, request, jsonify
from logicLayer import LogicLayer

ll = LogicLayer()
app = Flask(__name__)

'''
Test route to make sure the server is running
'''
@app.route('/', methods=['GET'])
def helloWorld():
    return json.dumps({"hello":"world"})

'''
Summary: Use this route to get a list of documents and scores for each n-gram provided.
Workflow: Ranking will receive a query request from the user and request relevant 
        documents from us after breaking the query into multiple n-grams.
From: Ranking
ERR handling: if the list of n-grams is null or non-existing, we will assume it is an 
        error and do no work.
'''
@app.route('/relevantDocs', methods=['POST'])
def relevantDocs():    
    if request.method == 'POST':      
        jsonData = request.get_json()
        result = ll.getDocs(jsonData)
        return result

'''
Summary: Use this route to add, update, or remove a document when information 
        pertaining to said document has changed.
Workflow: Crawling will determine if a document is to be added, updated, or removed,
        and Document Data Store will give us the data for the document that has been added, that needs to be removed, or both in the case of an update.
From: Document Data Store
ERR handling: if documentData is null rather than non-existing, we will assume it is 
        an error and do no work.
'''
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        jsonData = request.get_json()
        #if the request's remove or add section is non existant or null, do nothing
        if jsonData.get('remove') and jsonData['remove'] is not None:
            ll.removeDoc(jsonData['remove'])
        if jsonData.get('add') and jsonData['add'] is not None:
            ll.addDoc(jsonData['add'])
        return "update post recieved"

# helper functions should go below this line, but none yet


if __name__ == '__main__':
    app.debug = True
    app.run()
