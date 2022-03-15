import json 
import requests
import sys

from flask import Flask, request, jsonify
app = Flask(__name__)

# serverIPAddress = None 
# serverPortNumber = None

@app.route('/check_pan', methods=[ 'GET', 'POST'])
def receiver():
    #handle messages from the server
    if request.method == 'POST':
        msgFromServer = request.get_json(force=True) 

        print("Received from the server: ", msgFromServer)

        msgDict = json.loads(msgFromServer)

        serverAddress = f'http://{serverIPAddress}:{serverPortNumber}/'
        jsonObject = json.dumps(
            {
                "Acknowledgement": "Message from server received succefully",
                "SourceofMessage": msgDict["Message"]["Sender"],
                "MessageType": msgDict["Message"]["MessageType"]
            }
        )
        result = requests.post(serverAddress, json=jsonObject)

        print("Acknowledgement sent!: ", result)
    else:
        return "Get Method! Nothing Happended"

    return "Success!"

if __name__ == '__main__':

    # reading jsonfile
    jsonFile = open('./resources/config.json')
    jsonData = json.load(jsonFile)

    global serverIPAddress 
    global serverPortNumber

    serverIPAddress = jsonData['host']
    serverPortNumber = jsonData['port']

    app.run(host=sys.argv[1], port=sys.argv[2], debug=True)