import json 
import xmltodict
import requests
import sys

from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/foo', methods=['GET', 'POST'])
def source():
    xmlFile = open(messagePath)
    xmlData = xmlFile.read()
    xmlData = xmltodict.parse(xmlData)
    xmlFile.close()

    jsonData = json.dumps(xmlData)

    print("Message that is sent from source is: ", jsonData)

    serverAddress = f'http://{serverIPAddress}:{serverPortNumber}/'
    result = requests.post(serverAddress, json=jsonData)
    print("Message sent from source to server: ", result)
    return "Successs!"

if __name__ == '__main__':

    # reading jsonfile
    jsonFile = open('./resources/config.json')
    jsonData = json.load(jsonFile)

    global messagePath 
    global serverIPAddress 
    global serverPortNumber

    messagePath = './resources/message.xml'
    serverIPAddress = jsonData['host']
    serverPortNumber = jsonData['port']

    app.run(host=sys.argv[1], port=sys.argv[2], debug=True)