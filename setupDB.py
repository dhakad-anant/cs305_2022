import sqlite3

import datetime
from pytz import timezone 

class DBOperations:
    db = None 

    # Setting up connection
    def __init__(self, dbURL):
        try:
            self.db = sqlite3.connect(dbURL)
            print ("DB Connection setup successfully!")
        except:
            print("Error in DB Connection setup!")
        
    def showRoutingTableData(self):
        data = (self.db.execute('select * from routing')).fetchall()

        data = list(data)
        for row in data:
            print(row)

    def findReceiver(self, sender, messageType):
        data = self.db.execute('select Destination from routing where Sender=? and MessageType=?', [sender, messageType])
        data = list(data.fetchall())
        return data[0][0]
    
    def findRouteId(self, sender, messageType):
        data = self.db.execute('select RouteId from routing where Sender=? and MessageType=?', [sender, messageType])
        data = list(data.fetchall())
        return data[0][0]

    def recordLog(self, RouteId, EventType):
        print("*******************logging in database****************************************")
        EventTime = datetime.datetime.now().strftime("%a %b %d %H:%M:%S IST %Y")
        self.db.execute('insert into message_logs(RouteId, EventType, EventTime) values(?, ?, ?)', [RouteId, EventType, EventTime])
        self.db.commit()
        print(EventType, "*******************Log record successful!****************************************")

    def closeDBConnection(self):
        self.db.close()
        print("Connection closed successfully!!")