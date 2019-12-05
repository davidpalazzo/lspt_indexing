import json
import sqlite3
from flask import Flask, request, jsonify
from logicLayer import LogicLayer


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
        result = LogicLayer.getDocs(jsonData)
        print(result)
    return result

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        jsonData = request.get_json()
        print("update recieved: ",jsonData)
        if jsonData['remove']:
            print(jsonData['remove'])
            LogicLayer.removeDoc(jsonData['remove'])
        # #then
        if jsonData['add']:
            print(jsonData['add'])
            LogicLayer.addDoc(jsonData['add'])
        return "update post recieved"

# helper functions: none yet


if __name__ == '__main__':
    app.debug = True
    app.run()