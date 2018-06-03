import I2C_LCD_driver
import datetime
import time
import firebase_client


mylcd = I2C_LCD_driver.lcd()

def stream_handler(message):
    #print(message["event"]) # put
    #print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    #print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    data=message["data"]
    mylcd.lcd_clear()
    mylcd.lcd_display_string('CW: {0}'.format(data))

fbc=firebase_client.firebase_client()
db= fbc.getdb()
my_stream = db.child("realtime_data").stream(stream_handler)