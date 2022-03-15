import json 
import requests
from sympy import threaded

from setupDB import DBOperations

from flask import Flask, request
app = Flask(__name__)

# Database handler
configJSONData = None

@app.route('/', methods=['GET','POST'])
def serverSendingMessage():

    # Handling the post request
    if request.method == 'POST':
        inputMessage = request.get_json(force=True) 
        
        inputMessageDict = json.loads(inputMessage)
        
        if 'Acknowledgement' in inputMessage:
            print("Acknowledgement received!")
            print("SourceofMessage was: ",inputMessageDict["SourceofMessage"])
            print("MessageType was: ",inputMessageDict["MessageType"])
        else:
            db = DBOperations(configJSONData['db_url'])

            sender = inputMessageDict["Message"]["Sender"]
            messageType = inputMessageDict["Message"]["MessageType"]
            destinationAddress = db.findReceiver(sender, messageType)
            routeId = db.findRouteId(sender, messageType)

            print("Sender of Message: ", sender)
            print("messageType was: ", messageType)
            print("receiver was: ", destinationAddress)
            print("routeId was: ", routeId)

            # # recording received log
            # # db.recordLog(routeId, "RECEIVED")

            # print("Received Data from client: ", inputMessage)

            # # sending message received from the client to the receiver.
            # res = requests.post(destinationAddress, json=inputMessage)

            # # recording sent log
            # # db.recordLog(routeId, "SENT")

            # print("Message sent to receiver: ", res)

            # # close DB connection
            # db.closeDBConnection()
            # ----------------------------------

            # recording received log
            db.recordLog(routeId, "RECEIVED")

            print("Received Data from client: ", inputMessage)

            # recording sent log
            db.recordLog(routeId, "SENT")

            # close DB connection
            db.closeDBConnection()

            # sending message received from the client to the receiver.
            res = requests.post(destinationAddress, json=inputMessage)

            print("Message sent to receiver: ", res)
    else:
        return "Get Method! Nothing Happended"

    return 'Executed Successfully!'

if __name__ == '__main__':

    configJSONFile = open('./resources/config.json')
    configJSONData = json.load(configJSONFile)

    app.run(
        host=configJSONData['host'], 
        port=configJSONData['port'],
        debug=True,
        threaded=True
    )
