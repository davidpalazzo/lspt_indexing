import json
import sqlite3
from flask import Flask, request, jsonify
from logicLayer import LogicLayer

ll = LogicLayer()
app = Flask(__name__)

@app.route('/', methods=['GET'])
def helloWorld():
    return json.dumps({"hello":"world"})

@app.route('/relevantDocs', methods=['POST'])
def relevantDocs():
    print("received:", request)
    
    if request.method == 'POST':      
        jsonData = request.get_json()
        print("ngrams recieved: ",jsonData)
        result = ll.getDocs(jsonData)
        print("result is ", result)
    return result

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        jsonData = request.get_json()
        print("update recieved: ",jsonData)
        if jsonData.get('remove'):
            print(jsonData['remove'])
            ll.removeDoc(jsonData['remove'])
        # #then
        if jsonData.get('add'):
            print(jsonData['add'])
            ll.addDoc(jsonData['add'])
        return "update post recieved"

# helper functions: none yet


if __name__ == '__main__':
    app.debug = True
    app.run()
