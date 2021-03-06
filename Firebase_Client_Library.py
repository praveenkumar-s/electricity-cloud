import pyrebase
import sys


class firebase_client:
    def __init__(self):        
        config = {
        "apiKey": "dfa76d31d18d6b882d5c08bcd084182eb7313851",
        "authDomain": "electric-cloud.firebaseapp.com",
        "databaseURL": "https://electric-cloud.firebaseio.com",
        "storageBucket": "electric-cloud.appspot.com",
        "serviceAccount": "electric-cloud-firebase-adminsdk-xuxs4-dfa76d31d1.json"
        }
        self.firebase = pyrebase.initialize_app(config)
        self.firebase.auth()
    def getdb(self):
        return self.firebase.database()

    def putvalue(self, child, data):
        db= self.firebase.database()
        db.child(child).set(data)
    def getdata(self,tag):
        db= self.firebase.database()
        try:
            return db.child(tag).get().val()
        except:
            return None
